package com.osteoporosis;

import java.util.List;

public class BoneDensityAnalyzer {

    public String analyze(List<Double> data){

        double boneDensity = data.get(3);

        if(boneDensity < 0.60){

            return "High Risk of Osteoporosis";

        } else if(boneDensity < 0.75){

            return "Moderate Risk";

        } else{

            return "Low Risk";

        }

    }

}