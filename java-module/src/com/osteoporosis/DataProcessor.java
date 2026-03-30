package com.osteoporosis;

import java.util.ArrayList;
import java.util.List;

public class DataProcessor {

    public List<Double> processPatientData(
            int age,
            int gender,
            double bmi,
            double boneDensity,
            int calcium,
            int vitaminD
    ){

        List<Double> features = new ArrayList<>();

        features.add((double) age);
        features.add((double) gender);
        features.add(bmi);
        features.add(boneDensity);
        features.add((double) calcium);
        features.add((double) vitaminD);

        return features;
    }

}