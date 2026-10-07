import { useState } from "react";
import {
    Upload,
    FileArchive,
    BrainCircuit,
    Loader2,
    CheckCircle2,
    AlertTriangle,
    BarChart3,
} from "lucide-react";

import { analyzeProject } from "./services/api";

import "./App.css";


function App() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [selectedClass, setSelectedClass] = useState(null);


    // ==========================================
    // FILE SELECTION
    // ==========================================

    const handleFileChange = (event) => {

        const selectedFile = event.target.files[0];

        if (!selectedFile) {
            return;
        }

        if (!selectedFile.name.toLowerCase().endsWith(".zip")) {

            alert("Please select a ZIP file.");

            return;
        }

        setFile(selectedFile);
        setResult(null);
        setSelectedClass(null);
        setError("");
    };


    // ==========================================
    // ANALYZE PROJECT
    // ==========================================

    const handleAnalyze = async () => {

        if (!file) {

            alert("Please select a ZIP file first.");

            return;
        }

        try {

            setLoading(true);
            setError("");

            console.log("Uploading:", file.name);

            const data = await analyzeProject(file);

            console.log("Backend response:", data);

            setResult(data);

            // Select the first class automatically
            if (
                data.predictions &&
                data.predictions.length > 0
            ) {

                setSelectedClass(
                    data.predictions[0].Class
                );
            }

        } catch (err) {

            console.error(
                "Analysis failed:",
                err
            );

            setError(
                err.response?.data?.detail ||
                "Failed to analyze the project."
            );

        } finally {

            setLoading(false);
        }
    };


    // ==========================================
    // BACKEND DATA
    // ==========================================

    const predictions =
        result?.predictions || [];

    const featureVectors =
        result?.feature_vectors || [];


    // ==========================================
    // PRIORITY COUNTS
    // ==========================================

    const highCount =
        predictions.filter(
            (item) =>
                item.refactoring_priority === "HIGH"
        ).length;


    const mediumCount =
        predictions.filter(
            (item) =>
                item.refactoring_priority === "MEDIUM"
        ).length;


    const lowCount =
        predictions.filter(
            (item) =>
                item.refactoring_priority === "LOW"
        ).length;


    // ==========================================
    // SELECTED CLASS
    // ==========================================

    const selectedPrediction =
        predictions.find(
            (item) =>
                item.Class === selectedClass
        );


    const selectedFeatures =
        featureVectors.find(
            (item) =>
                item.Class === selectedClass
        );


    // ==========================================
    // PRIORITY STYLE
    // ==========================================

    const getPriorityClass = (priority) => {

        if (priority === "HIGH") {

            return "priority-high";
        }

        if (priority === "MEDIUM") {

            return "priority-medium";
        }

        return "priority-low";
    };


    // ==========================================
    // FORMAT PROBABILITY
    // ==========================================

    const formatPercentage = (value) => {

        if (
            value === undefined ||
            value === null
        ) {

            return "0%";
        }

        return `${(
            value * 100
        ).toFixed(1)}%`;
    };


    // ==========================================
    // RENDER
    // ==========================================

    return (

        <div className="app">


            {/* =================================
                NAVBAR
            ================================= */}

            <nav className="navbar">

                <div className="brand">

                    <BrainCircuit size={28} />

                    <span>
                        AI Refactoring System
                    </span>

                </div>

            </nav>


            {/* =================================
                MAIN
            ================================= */}

            <main className="main-container">


                {/* =================================
                    UPLOAD SECTION
                ================================= */}

                <section className="upload-section">


                    <div className="hero-icon">

                        <FileArchive size={48} />

                    </div>


                    <h1>
                        AI Refactoring System
                    </h1>


                    <p className="subtitle">

                        Analyze Java projects using
                        CK Metrics, SonarQube and
                        Machine Learning.

                    </p>


                    {/* UPLOAD BOX */}

                    <div
                        className="upload-box"
                        onClick={() =>
                            document
                                .getElementById(
                                    "fileInput"
                                )
                                .click()
                        }
                    >

                        <Upload size={40} />


                        <h3>

                            {file
                                ? file.name
                                : "Upload your Java project"}

                        </h3>


                        <span>

                            Select a .zip file

                        </span>


                        <input
                            id="fileInput"
                            type="file"
                            accept=".zip"
                            onChange={
                                handleFileChange
                            }
                            hidden
                        />

                    </div>


                    {/* ANALYZE BUTTON */}

                    <button
                        className="analyze-button"
                        onClick={handleAnalyze}
                        disabled={
                            !file ||
                            loading
                        }
                    >

                        {loading ? (

                            <>

                                <Loader2
                                    className="spin"
                                    size={20}
                                />

                                Analyzing...

                            </>

                        ) : (

                            <>

                                <BarChart3
                                    size={20}
                                />

                                Analyze Project

                            </>

                        )}

                    </button>


                    {/* ERROR */}

                    {error && (

                        <div className="error-message">

                            <AlertTriangle
                                size={20}
                            />

                            <span>
                                {error}
                            </span>

                        </div>

                    )}

                </section>


                {/* =================================
                    DASHBOARD
                ================================= */}

                {result &&
                    result.status === "success" && (

                        <section className="dashboard">


                            {/* SUCCESS MESSAGE */}

                            <div className="success-banner">

                                <CheckCircle2
                                    size={22}
                                />

                                <div>

                                    <strong>
                                        Analysis completed
                                        successfully
                                    </strong>

                                    <span>
                                        {result.project}
                                    </span>

                                </div>

                            </div>


                            {/* =================================
                                SUMMARY CARDS
                            ================================= */}

                            <div className="summary-grid">


                                <div className="summary-card">

                                    <span className="summary-label">
                                        Classes Analyzed
                                    </span>

                                    <strong>
                                        {
                                            predictions.length
                                        }
                                    </strong>

                                </div>


                                <div className="summary-card high-card">

                                    <span className="summary-label">
                                        HIGH Priority
                                    </span>

                                    <strong>
                                        {highCount}
                                    </strong>

                                </div>


                                <div className="summary-card medium-card">

                                    <span className="summary-label">
                                        MEDIUM Priority
                                    </span>

                                    <strong>
                                        {mediumCount}
                                    </strong>

                                </div>


                                <div className="summary-card low-card">

                                    <span className="summary-label">
                                        LOW Priority
                                    </span>

                                    <strong>
                                        {lowCount}
                                    </strong>

                                </div>

                            </div>


                            {/* =================================
                                PRIORITY TABLE
                            ================================= */}

                            <div className="dashboard-card">


                                <div className="section-header">

                                    <div>

                                        <h2>
                                            Refactoring Priority
                                        </h2>

                                        <p>
                                            Random Forest
                                            prediction for
                                            each class
                                        </p>

                                    </div>

                                </div>


                                <div className="table-container">

                                    <table>

                                        <thead>

                                            <tr>

                                                <th>
                                                    Class
                                                </th>

                                                <th>
                                                    Priority
                                                </th>

                                                <th>
                                                    HIGH
                                                </th>

                                                <th>
                                                    MEDIUM
                                                </th>

                                                <th>
                                                    LOW
                                                </th>

                                            </tr>

                                        </thead>


                                        <tbody>

                                            {predictions.map(
                                                (item) => (

                                                    <tr
                                                        key={
                                                            item.Class
                                                        }

                                                        className={
                                                            selectedClass ===
                                                            item.Class
                                                                ? "selected-row"
                                                                : ""
                                                        }

                                                        onClick={() =>
                                                            setSelectedClass(
                                                                item.Class
                                                            )
                                                        }
                                                    >

                                                        <td className="class-name">

                                                            {
                                                                item.Class
                                                            }

                                                        </td>


                                                        <td>

                                                            <span
                                                                className={`priority-badge ${getPriorityClass(
                                                                    item.refactoring_priority
                                                                )}`}
                                                            >

                                                                {
                                                                    item.refactoring_priority
                                                                }

                                                            </span>

                                                        </td>


                                                        <td>

                                                            {formatPercentage(
                                                                item
                                                                    .prediction_probabilities
                                                                    ?.HIGH
                                                            )}

                                                        </td>


                                                        <td>

                                                            {formatPercentage(
                                                                item
                                                                    .prediction_probabilities
                                                                    ?.MEDIUM
                                                            )}

                                                        </td>


                                                        <td>

                                                            {formatPercentage(
                                                                item
                                                                    .prediction_probabilities
                                                                    ?.LOW
                                                            )}

                                                        </td>

                                                    </tr>

                                                )
                                            )}

                                        </tbody>

                                    </table>

                                </div>

                            </div>


                            {/* =================================
                                CLASS DETAILS
                            ================================= */}

                            {selectedPrediction &&
                                selectedFeatures && (

                                    <div className="details-grid">


                                        {/* =========================
                                            METRICS
                                        ========================= */}

                                        <div className="dashboard-card">


                                            <div className="section-header">

                                                <div>

                                                    <h2>
                                                        {
                                                            selectedClass
                                                        }
                                                    </h2>

                                                    <p>
                                                        Class metrics
                                                        and model
                                                        prediction
                                                    </p>

                                                </div>


                                                <span
                                                    className={`priority-badge ${getPriorityClass(
                                                        selectedPrediction.refactoring_priority
                                                    )}`}
                                                >

                                                    {
                                                        selectedPrediction.refactoring_priority
                                                    }

                                                </span>

                                            </div>


                                            {/* CK METRICS */}

                                            <h3 className="metric-heading">

                                                CK Metrics

                                            </h3>


                                            <div className="metric-grid">

                                                <Metric
                                                    label="WMC"
                                                    value={
                                                        selectedFeatures.WMC
                                                    }
                                                />

                                                <Metric
                                                    label="CBO"
                                                    value={
                                                        selectedFeatures.CBO
                                                    }
                                                />

                                                <Metric
                                                    label="DIT"
                                                    value={
                                                        selectedFeatures.DIT
                                                    }
                                                />

                                                <Metric
                                                    label="NOC"
                                                    value={
                                                        selectedFeatures.NOC
                                                    }
                                                />

                                                <Metric
                                                    label="RFC"
                                                    value={
                                                        selectedFeatures.RFC
                                                    }
                                                />

                                                <Metric
                                                    label="LCOM"
                                                    value={
                                                        selectedFeatures.LCOM
                                                    }
                                                />

                                            </div>


                                            {/* SONAR METRICS */}

                                            <h3 className="metric-heading">

                                                SonarQube Metrics

                                            </h3>


                                            <div className="metric-grid">

                                                <Metric
                                                    label="Code Smells"
                                                    value={
                                                        selectedFeatures[
                                                            "Code Smells"
                                                        ]
                                                    }
                                                />

                                                <Metric
                                                    label="Vulnerabilities"
                                                    value={
                                                        selectedFeatures
                                                            .Vulnerabilities
                                                    }
                                                />

                                                <Metric
                                                    label="Bugs"
                                                    value={
                                                        selectedFeatures.Bugs
                                                    }
                                                />

                                                <Metric
                                                    label="Major Issues"
                                                    value={
                                                        selectedFeatures[
                                                            "Major Issues"
                                                        ]
                                                    }
                                                />

                                                <Metric
                                                    label="Minor Issues"
                                                    value={
                                                        selectedFeatures[
                                                            "Minor Issues"
                                                        ]
                                                    }
                                                />

                                                <Metric
                                                    label="Blocker Issues"
                                                    value={
                                                        selectedFeatures[
                                                            "Blocker Issues"
                                                        ]
                                                    }
                                                />

                                            </div>

                                        </div>


                                        {/* =========================
                                            PROBABILITY
                                        ========================= */}

                                        <div className="dashboard-card">


                                            <div className="section-header">

                                                <div>

                                                    <h2>
                                                        Prediction
                                                        Probability
                                                    </h2>

                                                    <p>
                                                        Random Forest
                                                        class probability
                                                    </p>

                                                </div>

                                            </div>


                                            <ProbabilityBar
                                                label="HIGH"
                                                value={
                                                    selectedPrediction
                                                        .prediction_probabilities
                                                        ?.HIGH
                                                }
                                            />


                                            <ProbabilityBar
                                                label="MEDIUM"
                                                value={
                                                    selectedPrediction
                                                        .prediction_probabilities
                                                        ?.MEDIUM
                                                }
                                            />


                                            <ProbabilityBar
                                                label="LOW"
                                                value={
                                                    selectedPrediction
                                                        .prediction_probabilities
                                                        ?.LOW
                                                }
                                            />

                                        </div>

                                    </div>

                                )}


                            {/* =================================
                                REFACTORING BENEFITS
                            ================================= */}

                            {selectedFeatures && (

                                <div className="dashboard-card benefits-card">


                                    <div className="section-header">

                                        <div>

                                            <h2>
                                                Refactoring Benefits
                                            </h2>

                                            <p>
                                                Expected benefits
                                                of improving{" "}
                                                <strong>
                                                    {
                                                        selectedClass
                                                    }
                                                </strong>
                                            </p>

                                        </div>

                                    </div>


                                    <div className="benefits-list">


                                        {/* CODE SMELLS */}

                                        {selectedFeatures[
                                            "Code Smells"
                                        ] > 0 && (

                                            <div className="benefit-item">

                                                <CheckCircle2
                                                    size={20}
                                                />

                                                <span>
                                                    Reduced code
                                                    smells
                                                </span>

                                            </div>

                                        )}


                                        {/* MAJOR ISSUES */}

                                        {selectedFeatures[
                                            "Major Issues"
                                        ] > 0 && (

                                            <div className="benefit-item">

                                                <CheckCircle2
                                                    size={20}
                                                />

                                                <span>
                                                    Improved code
                                                    quality
                                                </span>

                                            </div>

                                        )}


                                        {/* COMPLEXITY */}

                                        {(
                                            selectedFeatures.WMC >= 5 ||
                                            selectedFeatures.RFC >= 15
                                        ) && (

                                            <div className="benefit-item">

                                                <CheckCircle2
                                                    size={20}
                                                />

                                                <span>
                                                    Improved
                                                    maintainability
                                                </span>

                                            </div>

                                        )}


                                        {/* COUPLING */}

                                        {selectedFeatures.CBO >
                                            0 && (

                                            <div className="benefit-item">

                                                <CheckCircle2
                                                    size={20}
                                                />

                                                <span>
                                                    Reduced class
                                                    coupling
                                                </span>

                                            </div>

                                        )}


                                        {/* COHESION */}

                                        {selectedFeatures.LCOM >
                                            0 && (

                                            <div className="benefit-item">

                                                <CheckCircle2
                                                    size={20}
                                                />

                                                <span>
                                                    Improved class
                                                    cohesion
                                                </span>

                                            </div>

                                        )}


                                        {/* MINOR ISSUES */}

                                        {selectedFeatures[
                                            "Minor Issues"
                                        ] > 0 && (

                                            <div className="benefit-item">

                                                <CheckCircle2
                                                    size={20}
                                                />

                                                <span>
                                                    Improved code
                                                    consistency
                                                </span>

                                            </div>

                                        )}


                                        {/* NO ISSUES */}

                                        {selectedFeatures[
                                            "Code Smells"
                                        ] === 0 &&

                                            selectedFeatures[
                                                "Major Issues"
                                            ] === 0 &&

                                            selectedFeatures[
                                                "Minor Issues"
                                            ] === 0 &&

                                            selectedFeatures.CBO === 0 &&

                                            selectedFeatures.LCOM === 0 && (

                                                <div className="benefit-item">

                                                    <CheckCircle2
                                                        size={20}
                                                    />

                                                    <span>
                                                        Maintain a clean
                                                        and maintainable
                                                        code structure
                                                    </span>

                                                </div>

                                            )}

                                    </div>

                                </div>

                            )}

                        </section>

                    )}

            </main>

        </div>
    );
}


/* ==========================================
   METRIC COMPONENT
========================================== */

function Metric({
    label,
    value,
}) {

    return (

        <div className="metric-card">

            <span>
                {label}
            </span>

            <strong>
                {value ?? 0}
            </strong>

        </div>
    );
}


/* ==========================================
   PROBABILITY BAR
========================================== */

function ProbabilityBar({
    label,
    value,
}) {

    const percentage =
        (value || 0) * 100;


    return (

        <div className="probability">


            <div className="probability-header">

                <span>
                    {label}
                </span>

                <strong>
                    {percentage.toFixed(1)}%
                </strong>

            </div>


            <div className="probability-background">

                <div
                    className={`probability-fill probability-${label.toLowerCase()}`}
                    style={{
                        width: `${percentage}%`,
                    }}
                />

            </div>

        </div>
    );
}


export default App;