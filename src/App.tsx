import React, { useState } from "react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Textarea } from "./components/ui/textarea";
import axios from 'axios';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./components/ui/card";


// Define the Hazard type 
type Hazard = { 
  name: string;
  type: string;
  description: string;
  riskLevel: string;
  targetType: string;
  path: string;
};

const generateMitigations = async (hazard: Hazard) => {
  try {
    console.log('Sending request to generate mitigation for:', hazard.description);
    const response = await axios.post('http://localhost:5000/generate', {
      prompt: hazard.description
    });
    console.log('Received response:', response.data);
    return response.data.response;
  } catch (error) {
    console.error('Error generating mitigations:', error);
    return 'Error generating mitigation.';
  }
};


const HazardDetection = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [jsonData, setJsonData] = useState(null);
  const [hazards, setHazards] = useState<Hazard[]>([]);
  const [safetyText, setSafetyText] = useState("");
  const [mitigations, setMitigations] = useState<string[]>([]);
  const [showJsonContext, setShowJsonContext] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]; // Optional chaining in case no file is selected
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (loadEvent) => {
        try {
          const json = JSON.parse(loadEvent.target?.result as string); // Cast the result to a string
          setJsonData(json);
          console.log("Parsed JSON Data:", json);
        } catch (error) {
          console.error("Error parsing JSON:", error);
        }
      };
      reader.readAsText(file);
    }
  };
  
  

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0]; // Access the first file
    if (file.type === "application/json") {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (loadEvent) => {
        try {
          const json = JSON.parse(loadEvent.target?.result as string); // Cast the result to a string
          setJsonData(json);
          console.log("Parsed JSON Data:", json);
        } catch (error) {
          console.error("Error parsing JSON:", error);
        }
      };
      reader.readAsText(file);
    } else {
      console.error("Only JSON files are accepted");
    }
  };
  
  const detectHazards = (data: any) => {
    const hazards: Hazard[] = [];
    const stack: { obj: any; path: string }[] = [{ obj: data, path: "" }]; // Stack for deep traversal
  
    // Traverse the object tree
    while (stack.length > 0) {
      const { obj, path } = stack.pop()!; // Get current object and path
  
      if (typeof obj !== "object" || obj === null) continue;
  
      Object.keys(obj).forEach((key) => {
        const newPath = path ? `${path}.${key}` : key; // Construct new path for the object
  
        // Check if we are at the "Relations" array
        if (key.toLowerCase() === "relations" && Array.isArray(obj[key])) {
          obj[key].forEach((relation: any, index: number) => {
            // Look for "Hazards" in the relations
            if (relation[0] === "Hazards" && relation[1]?.Properties) {
              console.log(`Found Hazards at path: ${newPath}.Relations[${index}]`);
  
              // Extract the Properties array
              const properties = relation[1].Properties;
  
              // Initialize a new hazard object with default values
              const hazard: Hazard = {
                path: `${newPath}.Relations[${index}].Hazards`,
                name: "",
                type: "",
                description: "",
                riskLevel: "",
                targetType: ""
              };
  
              // Loop through the properties array to extract hazard details
              properties.forEach((property: any) => {
                const [propertyKey, propertyValue] = property;
                if (propertyValue && propertyValue.LocalValue) {
                  // Extract LocalValue for each key in the Properties array
                  if (propertyKey === "Name") {
                    hazard.name = propertyValue.LocalValue;
                  }
                  if (propertyKey === "Description") {
                    hazard.description = propertyValue.LocalValue;
                  }
                  if (propertyKey === "Type") {
                    hazard.type = propertyValue.LocalValue;
                  }
                  if (propertyKey === "Risk") {
                    hazard.riskLevel = propertyValue.LocalValue;
                  }
                  if (propertyKey === "TargetType") {
                    hazard.targetType = propertyValue.LocalValue;
                  }
                  // Log the property and its LocalValue for debugging
                  console.log(`Key: ${propertyKey}, LocalValue: ${propertyValue.LocalValue}`);
                }
              });
  
              // Add the hazard to the array
              hazards.push(hazard);
            }
          });
        }
  
        // Continue traversing if object or array found
        if (typeof obj[key] === "object" && obj[key] !== null) {
          stack.push({ obj: obj[key], path: newPath });
        }
      });
    }
  
    // Debugging the output to inspect the result
    console.log("Detected Hazards with Detailed Information:");
    hazards.forEach(hazard => {
      console.log(`Hazard Path: ${hazard.path}`);
      console.log(`Name: ${hazard.name}`);
      console.log(`Type: ${hazard.type}`);
      console.log(`Description: ${hazard.description}`);
      console.log(`Risk Level: ${hazard.riskLevel}`);
      console.log(`Target Type: ${hazard.targetType}`);
      console.log('---'); // Separator between hazards
    });
  
    return hazards;
  };

 
  const handleDetectHazards = () => {
    if (jsonData) {
      const detectedHazards = detectHazards(jsonData); // Pass the updated configuration
      setHazards(detectedHazards);
  
      const safetyText = detectedHazards
        .map(
          (hazard, index) =>
            `${index + 1}. ${hazard.name}:\n  - Hazard: ${hazard.description}\n  - Risk Level: ${hazard.riskLevel}\n  - Target Type: ${hazard.targetType}`
        )
        .join("\n\n");
      setSafetyText(safetyText);
    }
  }

  const handleGenerateMitigations = async () => {
    const mitigationsList = await Promise.all(
      hazards.map(async (hazard, index) => {
        const mitigation = await generateMitigations(hazard);
        return `${index + 1}. Hazard description:\n   ${mitigation}`;
      })
    );
    setMitigations(mitigationsList);
  };

  return (
    <div className="max-w-3xl mx-auto p-4"
    style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <Card>
        <CardHeader>
          <CardTitle>JSON Data Analysis for Hazard Detection</CardTitle>
          <CardDescription>
            Upload a JSON file to analyze and generate safety texts for
            automatic hazard detection.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            style={{
              flex: 1,
              border: "2px dashed #ccc",
              padding: "20px",
              textAlign: "center",
              cursor: "pointer", // Make the area clickable
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "40px",
            }}
            onDrop={handleDrop}
            onDragOver={(event) => event.preventDefault()}
          >
            <Label>Drag and drop a JSON file or upload from device</Label>
            <Input type="file" onChange={handleFileChange} accept=".json" />
          </div>
          {selectedFile && (
            <div className="mt-4"
              style={{alignItems: "center",
                justifyContent: "center"}}
            >
              <Button onClick={() => setShowJsonContext(!showJsonContext)}
                style={{
                  position: "absolute",
                  top: "210px",
                  right: "576px",
                  backgroundColor: "#f10f0f0",
                  border: "1px solid #ccc",
                  padding: "5px 10px",
                  cursor: "pointer",
                }}>
                {showJsonContext ? "Hide JSON Context" : "View JSON Context"}
              </Button>
              {showJsonContext && (
                <Textarea
                  value={JSON.stringify(jsonData, null, 2)}
                  readOnly
                  style={{
                  position: "absolute",
                  top: "250px",
                  right: "10px",
                  flex: 1,
                  border: "1px solid #ccc",
                  padding: "10px",
                  overflowY: "scroll",
                  width: "50%",
                  height: "280px",
                  resize: "none"
                  }}
                />
              )}
            </div>
          )}
          {jsonData && (
            <div className="mt-4">
              <Button onClick={handleDetectHazards}
              style={{
                position: "absolute",
                top: "210px",
                left: "27px",
                backgroundColor: "#f10f0f0",
                border: "1px solid #ccc",
                padding: "5px 10px",
                cursor: "pointer",
              }}>Detect Hazards</Button>
              {safetyText && (
                <div style={{ marginTop: "40px" }}>
                  <h2 className="text-lg font-bold">Detected Hazards:</h2>
                  <Textarea value={safetyText} readOnly style={{width: "45%", border: "1px solid #ccc", height: "156px", padding: "10px", fontSize: "14px", resize: "none"}} />
                </div>
              )}
            </div>
          )}
          {hazards.length > 0 && (
            <div className="mt-4">
              <Button onClick={handleGenerateMitigations}
              style={{
                position: "absolute",
                top: "475px",
                left: "27px",
                backgroundColor: "#f10f0f0",
                border: "1px solid #ccc",
                padding: "5px 10px",
                cursor: "pointer",
              }}>
                Generate Safety Texts
              </Button>
              {mitigations.length > 0 && (
                <div style={{ marginTop: "40px" }}>
                  <h2 className="text-lg font-bold">Detailed Description of Hazards with Mitigations:</h2>
                  <Textarea
                    value={mitigations.join("\n\n")}
                    readOnly
                    style={{width: "100%", border: "1px solid #ccc", height: "350px", padding: "10px", fontSize: "16px", resize: "none"}}
                  />
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default HazardDetection;
