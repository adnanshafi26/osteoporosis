package com.osteoporosis;

import java.util.List;

public class ReportGenerator {

    public void generateReport(List<Double> data, String result){

        System.out.println("------ Osteoporosis Screening Report ------");

        System.out.println("Age: " + data.get(0));
        System.out.println("Gender: " + data.get(1));
        System.out.println("BMI: " + data.get(2));
        System.out.println("Bone Density: " + data.get(3));
        System.out.println("Calcium Intake: " + data.get(4));
        System.out.println("Vitamin D Level: " + data.get(5));

        System.out.println("--------------------------------------------");

        System.out.println("AI Risk Assessment: " + result);

        System.out.println("--------------------------------------------");

    }

}