package com.regnosys.rosetta.generators.sample;

import java.io.File;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;

import com.regnosys.rosetta.generators.test.TestHelper;
import com.regnosys.rosetta.rosetta.RosettaModel;

public class RosettaCodeGenerator {
    private final TestHelper<SampleCodeGenerator> helper;
    private final SampleCodeGenerator generator;

    public RosettaCodeGenerator() {
        this.generator = new SampleCodeGenerator();
        this.helper = new TestHelper<>(generator);
    }

    public void generateCode(String rosettaFilePath, String outputDirectory) {
        try {
            System.out.println("Starting code generation...");
            System.out.println("Input file: " + rosettaFilePath);
            System.out.println("Output directory: " + outputDirectory);
            
            // Load and parse the Rosetta file using TestHelper
            File file = new File(rosettaFilePath);
            System.out.println("Reading from file: " + file.getAbsolutePath());
            
            URL fileUrl = file.toURI().toURL();
            RosettaModel model = helper.parse(fileUrl);
            System.out.println("Successfully parsed Rosetta model");
            
            // Generate the code
            Map<String, ? extends CharSequence> generatedFiles = generator.generate(model.eResource(), model, model.getVersion());
            System.out.println("Number of files to generate: " + generatedFiles.size());

            // Create output directory if it doesn't exist
            Path outputPath = Paths.get(outputDirectory);
            Files.createDirectories(outputPath);
            System.out.println("Created output directory: " + outputPath.toAbsolutePath());

            // Save each generated file
            for (Map.Entry<String, ? extends CharSequence> entry : generatedFiles.entrySet()) {
                String relativePath = entry.getKey();
                String content = entry.getValue().toString();
                
                // Create full path for output file
                Path fullPath = outputPath.resolve(relativePath);
                
                // Create parent directories if they don't exist
                Files.createDirectories(fullPath.getParent());
                
                // Write the content to the file
                Files.writeString(fullPath, content);
                System.out.println("Generated file: " + fullPath.toAbsolutePath());
            }
            System.out.println("Code generation completed successfully!");
        } catch (Exception e) {
            System.err.println("Error during code generation: " + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("Failed to generate code from Rosetta file: " + rosettaFilePath, e);
        }
    }

    public static void main(String[] args) {
        // Use the sample.rosetta file which has proper Data elements
        String rosettaFilePath = "sample\\src\\test\\resources\\rosetta\\regulation-cftc-rewrite-type-2.rosetta";
        String outputDirectory = "generated-code";

        RosettaCodeGenerator generator = new RosettaCodeGenerator();
        generator.generateCode(rosettaFilePath, outputDirectory);
        
        System.out.println("Code generation completed. Check the 'generated-code' directory for output files.");
    }
} 