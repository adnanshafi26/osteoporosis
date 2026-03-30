package com.osteoporosis;

import java.util.List;

public class MainTest {

    public static void main(String[] args) {

        DataProcessor processor = new DataProcessor();
        BoneDensityAnalyzer analyzer = new BoneDensityAnalyzer();
        ReportGenerator report = new ReportGenerator();

        List<Double> patientData = processor.processPatientData(
                65,
                0,
                22.0,
                0.55,
                800,
                20
        );

        String result = analyzer.analyze(patientData);

        report.generateReport(patientData, result);

    }

}