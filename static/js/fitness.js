document.addEventListener("DOMContentLoaded", function() {
    // DOM Elements
    const goalSelect = document.getElementById("goal");
    const bodyTypeSelect = document.getElementById("bodyType");
    const severitySelect = document.getElementById("severity");
    const loadingSpinner = document.getElementById("loadingSpinner");
    const planResultsEl = document.getElementById("planResults");

    // Load fitness data from JSON file
    fetch('data/fitness_data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(fitnessData => {
            // Populate goal select dropdown
            function populateGoalSelect() {
                goalSelect.innerHTML = '<option value="">Select your goal</option>';
                Object.keys(fitnessData).forEach(goal => {
                    const option = document.createElement("option");
                    option.value = goal;
                    option.textContent = formatText(goal);
                    goalSelect.appendChild(option);
                });
            }

            // When goal changes, update body type options
            goalSelect.addEventListener("change", function() {
                const selectedGoal = this.value;
                bodyTypeSelect.innerHTML = '<option value="">Select body type</option>';
                severitySelect.innerHTML = '<option value="">Select severity</option>';
                clearResults();

                if (!selectedGoal) return;

                // Handle "all" body type case
                if (fitnessData[selectedGoal].all) {
                    const option = document.createElement("option");
                    option.value = "all";
                    option.textContent = "All Types";
                    bodyTypeSelect.appendChild(option);
                } else {
                    // Add specific body types
                    Object.keys(fitnessData[selectedGoal]).forEach(bodyType => {
                        const option = document.createElement("option");
                        option.value = bodyType;
                        option.textContent = formatText(bodyType);
                        bodyTypeSelect.appendChild(option);
                    });
                }
            });

            // When body type changes, update severity options
            bodyTypeSelect.addEventListener("change", function() {
                const selectedGoal = goalSelect.value;
                const selectedBodyType = this.value;
                severitySelect.innerHTML = '<option value="">Select severity</option>';
                clearResults();

                if (!selectedGoal || !selectedBodyType) return;

                // Get available severities
                const severities = fitnessData[selectedGoal][selectedBodyType] 
                    ? Object.keys(fitnessData[selectedGoal][selectedBodyType]) 
                    : [];

                severities.forEach(severity => {
                    const option = document.createElement("option");
                    option.value = severity;
                    option.textContent = formatText(severity);
                    severitySelect.appendChild(option);
                });
            });

            // When severity changes, generate the plan
            severitySelect.addEventListener("change", function() {
                const selectedGoal = goalSelect.value;
                const selectedBodyType = bodyTypeSelect.value;
                const selectedSeverity = this.value;

                if (!selectedGoal || !selectedBodyType || !selectedSeverity) return;

                generatePlan(selectedGoal, selectedBodyType, selectedSeverity);
            });

            // Generate the fitness plan
            function generatePlan(goal, bodyType, severity) {
                showLoading();
                
                setTimeout(() => {
                    try {
                        // Get the specific plan
                        const plan = fitnessData[goal][bodyType][severity];
                        
                        // Show plan details
                        showPlanDetails(plan, goal);
                    } catch (error) {
                        console.error("Error generating plan:", error);
                        showError("Failed to generate workout plan. Please try different options.");
                    } finally {
                        hideLoading();
                    }
                }, 500);
            }

            // Show detailed plan information
            function showPlanDetails(plan, goal) {
                let html = `
                  <div class="weekly-plan">
                    <h4><i class="fas fa-calendar-week me-2"></i>Weekly Workout Plan</h4>
                    <div class="row g-3">`;
              
                // Add weekly plan days
                plan.weekly_plan.forEach(dayPlan => {
                  html += `
                    <div class="col-md-6">
                      <div class="day-plan">
                        <h5>${dayPlan.day}</h5>
                        <div class="routine-details">
                          ${dayPlan.routine.split("\n").map(item => `<p>${item}</p>`).join("")}
                          ${dayPlan.benefits ? `<p class="benefit"><strong>Benefits:</strong> ${dayPlan.benefits}</p>` : ''}
                          ${dayPlan.tips ? `<p class="tip"><strong>Tip:</strong> ${dayPlan.tips}</p>` : ''}
                        </div>
                      </div>
                    </div>`;
                });
              
                html += `
                    </div>
                  </div>
                  <div class="progression-plan">
                    <h4><i class="fas fa-chart-line me-2"></i>Progression Plan</h4>`;
              
                // Add progression phases
                for (const [phase, details] of Object.entries(plan.progression)) {
                    // Safely format phase name
                    const phaseName = formatText(phase.replace(/_/g, ' ')) || 'Phase';
                    
                    // Safely get weeks with fallback
                    const weeksDisplay = details.weeks ? `(${details.weeks})` : '';
                    
                    // Safely get focus with fallback
                    const focusDisplay = details.focus || 'Focus not specified';
                    
                    // Build actions HTML only if actions exist
                    const actionsHtml = details.actions && details.actions.length > 0 ? `
                      <div class="progression-actions">
                        <strong>Actions:</strong>
                        <ul>${details.actions.map(action => `<li>${action}</li>`).join('')}</ul>
                      </div>` : '';
                    
                    // Build metrics HTML only if metrics exist
                    const metricsHtml = details.metrics ? `
                      <p><strong>Track:</strong> ${details.metrics}</p>` : '';
                  
                    html += `
                      <div class="progression-phase">
                        <h5>${phaseName} ${weeksDisplay}</h5>
                        <p><strong>Focus:</strong> ${focusDisplay}</p>
                        ${actionsHtml}
                        ${metricsHtml}
                      </div>`;
                  }
              
                // Add nutrition tips if available
                if (plan.nutrition_tips) {
                  html += `
                  <div class="nutrition-tips">
                    <h4><i class="fas fa-utensils me-2"></i>Nutrition Tips</h4>
                    <ul>${plan.nutrition_tips.map(tip => `<li>${tip}</li>`).join('')}</ul>
                  </div>`;
                }
              
                html += `</div>`;
              
                planResultsEl.innerHTML = html;
              }

            // Initialize the goal dropdown
            populateGoalSelect();
        })
        .catch(error => {
            console.error('Error loading fitness data:', error);
            showError("Failed to load workout data. Please try again later.");
        });

    // Format text for display (convert snake_case to Title Case)
    function formatText(text) {
        return text.split("_")
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
    }

    // UI Helper Functions
    function showLoading() {
        loadingSpinner.style.display = "block";
        planResultsEl.innerHTML = "";
    }

    function hideLoading() {
        loadingSpinner.style.display = "none";
    }

    function showError(message) {
        planResultsEl.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                ${message}
            </div>
        `;
    }

    function clearResults() {
        planResultsEl.innerHTML = "";
    }
});