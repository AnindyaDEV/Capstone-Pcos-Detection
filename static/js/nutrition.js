// Search food nutrition information with enhanced UI
function searchFood() {
  const food = $("#foodInput").val().trim().toLowerCase();
  if (!food) {
    showAlert("Please enter a food item", "warning");
    return;
  }

  // Show loading state
  $("#nutritionResult").html(`
    <div class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Searching nutrition data for ${food}...</p>
    </div>
  `);

  // Get icon based on food type
  const foodIcon = getFoodIcon(food);

  $.ajax({
    url: "/get_nutrition",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ food }),
    success: (data) => {
      if (data.error) {
        showAlert(data.error, "danger", "#nutritionResult");
      } else {
        const html = `
          <div class="nutrition-card p-4 rounded-3 shadow-sm">
            <div class="text-center mb-3">
              ${foodIcon}
              <h4 class="mt-2">${capitalizeFirstLetter(data.name)}</h4>
            </div>
            <div class="row text-center">
              <div class="col-md-3 mb-3">
                <div class="nutrition-value bg-primary text-white p-3 rounded">
                  <h3>${data.calories}</h3>
                  <p class="mb-0">Calories</p>
                  <small class="opacity-75">kcal</small>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="nutrition-value bg-secondary text-white p-3 rounded">
                  <h3>${data.protein}</h3>
                  <p class="mb-0">Protein</p>
                  <small class="opacity-75">g</small>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="nutrition-value bg-accent text-dark p-3 rounded">
                  <h3>${data.carbs}</h3>
                  <p class="mb-0">Carbs</p>
                  <small class="opacity-75">g</small>
                </div>
              </div>
              <div class="col-md-3 mb-3">
                <div class="nutrition-value bg-light p-3 rounded">
                  <h3>${data.fat}</h3>
                  <p class="mb-0">Fat</p>
                  <small class="opacity-75">g</small>
                </div>
              </div>
            </div>
          </div>
        `;
        $("#nutritionResult").html(html);
      }
    },
    error: (xhr) => {
      const errorMsg = xhr.responseJSON?.error || "Failed to fetch nutrition data";
      showAlert(errorMsg, "danger", "#nutritionResult");
    }
  });
}

// Helper function to get appropriate food icon
function getFoodIcon(food) {
  const foodIcons = {
    // Fruits
    apple: '<i class="fas fa-apple-alt fa-3x text-success"></i>',
    banana: '<i class="fas fa-banana fa-3x text-warning"></i>',
    orange: '<i class="fas fa-orange fa-3x text-warning"></i>',
    grape: '<i class="fas fa-grapes fa-3x text-purple"></i>',
    berry: '<i class="fas fa-berry fa-3x text-danger"></i>',
    lemon: '<i class="fas fa-lemon fa-3x text-warning"></i>',
    watermelon: '<i class="fas fa-watermelon fa-3x text-success"></i>',
    
    // Vegetables
    carrot: '<i class="fas fa-carrot fa-3x text-orange"></i>',
    broccoli: '<i class="fas fa-broccoli fa-3x text-success"></i>',
    salad: '<i class="fas fa-salad fa-3x text-success"></i>',
    pepper: '<i class="fas fa-pepper-hot fa-3x text-danger"></i>',
    
    // Protein sources
    egg: '<i class="fas fa-egg fa-3x text-warning"></i>',
    chicken: '<i class="fas fa-drumstick-bite fa-3x text-muted"></i>',
    fish: '<i class="fas fa-fish fa-3x text-info"></i>',
    beef: '<i class="fas fa-hamburger fa-3x text-danger"></i>',
    pork: '<i class="fas fa-bacon fa-3x text-danger"></i>',
    
    // Dairy
    milk: '<i class="fas fa-glass-whiskey fa-3x text-light"></i>',
    cheese: '<i class="fas fa-cheese fa-3x text-warning"></i>',
    yogurt: '<i class="fas fa-blender fa-3x text-light"></i>',
    
    // Grains
    bread: '<i class="fas fa-bread-slice fa-3x text-warning"></i>',
    rice: '<i class="fas fa-bowl-rice fa-3x text-light"></i>',
    pasta: '<i class="fas fa-pasta fa-3x text-light"></i>',
    
    // Default food icon
    default: '<i class="fas fa-utensils fa-3x text-primary"></i>'
  };

  // Check for matches in the food name
  for (const [keyword, icon] of Object.entries(foodIcons)) {
    if (food.includes(keyword)) {
      return icon;
    }
  }
  
  return foodIcons.default;
}

// Helper function to capitalize first letter
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
// Handle macro calculation form with enhanced UI
$("#macroForm").submit(function (e) {
  e.preventDefault();
  
  // Validate form
  const formData = Object.fromEntries(new FormData(this));
  if (!formData.weight || !formData.height || !formData.age) {
    showAlert("Please fill all required fields", "warning");
    return;
  }

  // Show loading state
  $("#macro-output").html(`
    <div class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Calculating your macronutrients...</p>
    </div>
  `);

  $.ajax({
    url: "/calculate_macros",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(formData),
    success: (data) => {
      const html = `
        <div class="macro-result p-4 rounded-3 shadow-sm">
          <h4 class="text-center mb-4">
            <i class="fas fa-chart-pie me-2"></i>Your Daily Macros
          </h4>
          <div class="row text-center g-3">
            <div class="col-md-3">
              <div class="p-3 rounded bg-primary bg-opacity-10">
                <h2 class="text-primary">${data.calories}</h2>
                <p class="mb-0">Calories</p>
                <small class="text-muted">kcal/day</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-3 rounded bg-secondary bg-opacity-10">
                <h2 class="text-secondary">${data.protein}</h2>
                <p class="mb-0">Protein</p>
                <small class="text-muted">g/day</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-3 rounded bg-accent bg-opacity-10">
                <h2 class="text-accent">${data.carbs}</h2>
                <p class="mb-0">Carbs</p>
                <small class="text-muted">g/day</small>
              </div>
            </div>
            <div class="col-md-3">
              <div class="p-3 rounded bg-light">
                <h2 class="text-dark">${data.fat}</h2>
                <p class="mb-0">Fat</p>
                <small class="text-muted">g/day</small>
              </div>
            </div>
          </div>
        </div>
      `;
      $("#macro-output").html(html);
      
      // Store the calculated calories for meal planning
      $("#macro-output").data("calories", data.calories);
    },
    error: (xhr) => {
      const errorMsg = xhr.responseJSON?.error || "Failed to calculate macros";
      showAlert(errorMsg, "danger", "#macro-output");
    }
  });
});

// Generate weekly meal plan with enhanced UI
function generateMealPlan() {
  // Get the stored calories from the data attribute we set after macro calculation
  const calories = $("#macro-output").data("calories");
  
  if (!calories) {
    showToast("Please calculate your macros first by submitting the form above", "warning");
    return;
  }

  // Show loading state
  $('#mealPlanResult').html(`
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Creating your personalized meal plan...</p>
    </div>
  `);

  $.ajax({
    url: "/meal_plan",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ calories }),
    success: (response) => {
      // Extract the actual meal plan data from the response
      const data = Array.isArray(response) ? response[0] : response;
      
      if (!data || typeof data !== 'object' || Object.keys(data).length === 0) {
        showAlert("No valid meal plan data received", "danger", "#mealPlanResult");
        return;
      }

      const dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
      const mealOrder = ["Breakfast", "Mid-Morning Snack", "Lunch", "Evening Snack", "Dinner"];

      let html = '<div class="row g-4">';

      dayOrder.forEach(day => {
        if (!data[day]) {
          console.warn(`Missing data for day: ${day}`);
          return;
        }

        let dayCalories = 0;
        let dayMacros = { protein: 0, fat: 0, carbs: 0 };

        // Build meals list
        let mealsHtml = '';
        mealOrder.forEach(mealType => {
          const meal = data[day][mealType];
          if (!meal) {
            console.warn(`Missing ${mealType} for ${day}`);
            return;
          }

          // Safely add nutrition values (handle potential undefined)
          dayCalories += Number(meal.calories) || 0;
          dayMacros.protein += Number(meal.protein) || 0;
          dayMacros.fat += Number(meal.fat) || 0;
          dayMacros.carbs += Number(meal.carbs) || 0;

          // Add different icons for different meal types
          const mealIcon = {
            'Breakfast': '🥞',
            'Mid-Morning Snack': '🍎',
            'Lunch': '🍲',
            'Evening Snack': '🥨',
            'Dinner': '🍽️'
          }[mealType] || '🍴';

          mealsHtml += `
            <div class="meal-item mb-3 p-3 border rounded">
              <div class="d-flex justify-content-between align-items-center">
                <h6 class="mb-0 text-primary">${mealIcon} ${mealType}</h6>
                <span class="badge bg-light text-dark">${meal.calories || 0} kcal</span>
              </div>
              <h5 class="my-2">${meal.title || 'No title'}</h5>
              <div class="macros-grid">
                <div class="macro-item">
                  <span class="macro-value">${meal.protein || 0}g</span>
                  <span class="macro-label">Protein</span>
                </div>
                <div class="macro-item">
                  <span class="macro-value">${meal.carbs || 0}g</span>
                  <span class="macro-label">Carbs</span>
                </div>
                <div class="macro-item">
                  <span class="macro-value">${meal.fat || 0}g</span>
                  <span class="macro-label">Fat</span>
                </div>
              </div>
            </div>
          `;
        });

        // Add day card
        html += `
          <div class="col-lg-6">
            <div class="day-card card h-100">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">${day}</h5>
                <span class="badge bg-primary">${dayCalories} kcal</span>
              </div>
              <div class="card-body">
                ${mealsHtml}
                <div class="day-total mt-3 p-2 bg-light rounded text-center">
                  <div class="d-flex justify-content-around">
                    <div>
                      <small class="text-muted">Protein</small>
                      <div class="fw-bold">${dayMacros.protein}g</div>
                    </div>
                    <div>
                      <small class="text-muted">Carbs</small>
                      <div class="fw-bold">${dayMacros.carbs}g</div>
                    </div>
                    <div>
                      <small class="text-muted">Fat</small>
                      <div class="fw-bold">${dayMacros.fat}g</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
      });

      html += '</div>';
      $('#mealPlanResult').html(html).data("mealPlan", data);
      $("#savePlanBtn").removeClass('d-none');
      $("#saveStatus").html("");
    },
    error: (xhr) => {
      const errorMsg = xhr.responseJSON?.error || "Failed to generate meal plan";
      showAlert(errorMsg, "danger", "#mealPlanResult");
    }
  });
}

// Save the generated meal plan with enhanced UI
$("#savePlanBtn").on("click", function() {
  const $btn = $(this);
  const planData = $("#mealPlanResult").data("mealPlan");
  
  if (!planData) {
    showToast("No meal plan to save. Please generate one first.", "warning");
    return;
  }

  // Show loading state on button
  $btn.prop("disabled", true).html(`
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Saving...
  `);

  $("#saveStatus").html(`
    <div class="alert alert-info">
      <i class="fas fa-spinner fa-spin me-2"></i> Preparing your meal plan PDF...
    </div>
  `);

  $.ajax({
    url: "/save_meal_plan",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ meal_plan: planData }),
    success: (res) => {
      $btn.prop("disabled", false).html(`
        <i class="fas fa-file-pdf me-1"></i> Save as PDF
      `);
      
      $("#saveStatus").html(`
        <div class="alert alert-success">
          <i class="fas fa-check-circle me-2"></i> ${res.message}
        </div>
      `);
      
      if (res.pdf_url) {
        $("#viewPlanBtn")
          .attr("href", res.pdf_url)
          .removeClass('d-none')
          .html(`<i class="fas fa-eye me-1"></i> View PDF`);
      }
    },
    error: (xhr) => {
      $btn.prop("disabled", false).html(`
        <i class="fas fa-file-pdf me-1"></i> Save as PDF
      `);
      
      const err = xhr.responseJSON?.error || "Failed to save meal plan";
      showToast(err, "danger", "#saveStatus");
    }
  });
});
$("#savePlanBtn").on("click", function() {
  const $btn = $(this);
  const planData = $("#mealPlanResult").data("mealPlan");
  
  if (!planData) {
    showToast("No meal plan to save. Please generate one first.", "warning");
    return;
  }

  // Show loading state on button
  $btn.prop("disabled", true).html(`
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Saving...
  `);

  // Show saving status
  $("#saveStatus").html(`
    <div class="alert alert-info">
      <i class="fas fa-spinner fa-spin me-2"></i> Preparing your meal plan PDF...
    </div>
  `);

  // Hide view button while saving
  $("#viewPlanBtn").addClass('d-none');

  $.ajax({
    url: "/save_meal_plan",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ meal_plan: planData }),
    success: (res) => {
      // Reset save button
      $btn.prop("disabled", false).html(`
        <i class="fas fa-file-pdf me-1"></i> Save as PDF
      `);
      
      // Show success message
      $("#saveStatus").html(`
        <div class="alert alert-success">
          <i class="fas fa-check-circle me-2"></i> ${res.message}
        </div>
      `);
      
      // Show view button if PDF URL exists
      if (res.pdf_url) {
        $("#viewPlanBtn")
          .attr("href", res.pdf_url)
          .removeClass('d-none')
          .on('click', function(e) {
            // Open in new tab
            window.open(res.pdf_url, '_blank');
            e.preventDefault();
          });
      }
    },
    error: (xhr) => {
      // Reset save button
      $btn.prop("disabled", false).html(`
        <i class="fas fa-file-pdf me-1"></i> Save as PDF
      `);
      
      // Show error message
      const err = xhr.responseJSON?.error || "Failed to save meal plan";
      $("#saveStatus").html(`
        <div class="alert alert-danger">
          <i class="fas fa-exclamation-circle me-2"></i> ${err}
        </div>
      `);
    }
  });
});

// Helper function to show toast notifications
// Modify the showToast function to not remove existing toasts immediately
function showToast(message, type = "info") {
  const toastId = 'toast-' + Date.now();
  const toastColors = {
    'info': 'bg-primary text-white',
    'success': 'bg-success text-white',
    'warning': 'bg-warning text-dark',
    'danger': 'bg-danger text-white'
  };
  
  const toastHtml = `
    <div id="${toastId}" class="toast show mb-2" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header ${toastColors[type] || 'bg-primary text-white'}">
        <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
        <small class="text-white">Just now</small>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        ${message}
      </div>
    </div>
  `;
  
  $('.position-fixed').append(toastHtml);
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    $(`#${toastId}`).toast('hide');
  }, 5000);
  
  // Remove toast after it's hidden
  $(`#${toastId}`).on('hidden.bs.toast', function() {
    $(this).remove();
  });
}
  



// Initialize tooltips
$(function () {
  $('[data-bs-toggle="tooltip"]').tooltip();
});