#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <activity_detector_inferencing.h> // Edge Impulse SDK library

// Constants
#define CONVERT_G_TO_MS2    9.80665f
#define MAX_ACCEPTED_RANGE  2.0f  // ±2g range for higher sensitivity

// Create instance for ADXL345 accelerometer
Adafruit_ADXL345_Unified lis = Adafruit_ADXL345_Unified(12345);

// Buffer for storing accelerometer data
static float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = { 0 };
static float inference_buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE];

// Function to print buffer content for debugging
void printBuffer(float* buf, int size) {
    Serial.print("Buffer content: ");
    for (int i = 0; i < size; i++) {
        Serial.print(buf[i], 4);  // Print with 4 decimal places for clarity
        Serial.print(" ");
    }
    Serial.println();
}

void setup() {
    // Initialize serial communication for debugging
    Serial.begin(115200);
    while (!Serial);  // Wait for serial connection

    // Initialize the ADXL345 accelerometer
    if (!lis.begin()) {
        Serial.println("Failed to initialize ADXL345!");
        while (1);  // Stay stuck here if sensor initialization fails
    } else {
        Serial.println("ADXL345 initialized successfully.");
    }

    // Set the accelerometer's range
    lis.setRange(ADXL345_RANGE_2_G);  // ±2g for higher sensitivity
    lis.setDataRate(ADXL345_DATARATE_100_HZ);  // Data rate to 100Hz

    // Check the configuration
    if (EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME != 3) {
        Serial.println("ERROR: EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME should be 3.");
        return;
    }

    // Print sensor initialization info
    Serial.println("Starting inference...");
}

float getSign(float number) {
    return (number >= 0.0) ? 1.0 : -1.0;
}

void runInference() {
    // Roll the buffer to make space for new data (roll by -3, so the last 3 entries are overwritten)
    numpy::roll(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, -3);

    // Read accelerometer values
    sensors_event_t event;
    lis.getEvent(&event);

    // Add new data to the buffer (X, Y, Z acceleration)
    buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3] = event.acceleration.x;
    buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 2] = event.acceleration.y;
    buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 1] = event.acceleration.z;

    // Ensure that data doesn't exceed the maximum range (±2g)
    for (int i = 0; i < 3; i++) {
        if (fabs(buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3 + i]) > MAX_ACCEPTED_RANGE) {
            buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3 + i] = getSign(buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3 + i]) * MAX_ACCEPTED_RANGE;
        }
    }

    // Convert accelerometer values from g to m/s²
    buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3] *= CONVERT_G_TO_MS2;
    buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 2] *= CONVERT_G_TO_MS2;
    buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 1] *= CONVERT_G_TO_MS2;

    // Print the buffer content for debugging
    printBuffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE);

    // Now process the buffer for classification
    signal_t signal;
    int err = numpy::signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
    if (err != 0) {
        Serial.printf("Failed to create signal from buffer (%d)\n", err);
        return;
    }

    // Run the classifier
    ei_impulse_result_t result = { 0 };
    err = run_classifier(&signal, &result, true);  // Set to true for debug output
    if (err != EI_IMPULSE_OK) {
        Serial.printf("Error running classifier: (%d)\n", err);
        return;
    }

    // Print the inference results
    Serial.printf("Predictions (DSP: %d ms., Classification: %d ms., Anomaly: %d ms.):\n",
                  result.timing.dsp, result.timing.classification, result.timing.anomaly);

    // Print each class prediction
   for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
        Serial.printf("%s: %.5f\n", result.classification[ix].label, result.classification[ix].value);
    }
#if EI_CLASSIFIER_HAS_ANOMALY == 1
    Serial.printf("Anomaly score: %.3f\n", result.anomaly);
#endif
}

void loop() {
    // Run inference periodically
    runInference();
    delay(500);
}
