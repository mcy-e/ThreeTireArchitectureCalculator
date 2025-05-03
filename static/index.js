const display = document.getElementById("display");
const limitModal = document.getElementById("limitModal");

//*basic calculator functions
function appendToDisplay(input) {
  display.value += input;
}

function clearDisplay() {
  display.value = "";
}
function backspace() {
    display.value = display.value.slice(0, -1);
}
function calculate() {

    //*check if we're in scientific mode
        const scientificMode = document.getElementById('scientificKeys').classList.contains('active');
        
        if (scientificMode) {
            // In scientific mode: just add "=" to the display
            appendToDisplay('=');
            return; // Exit without calculating
    }
        
  try {
    //*for basic calculations continue to use eval
    if (!display.value.includes("x")) {
      //*replace pi and e if they are entered before evaluation
      let expression = display.value
        .replace(/pi/g, Math.PI)
        .replace(/e/g, Math.E);

      display.value = eval(expression);
    } else {
      //*if there's an 'x' in the expression, notify the user to use scientific functions
      alert("Use the scientific operations for expressions with variables.");
    }
  } catch (error) {
    display.value = "Error";
  }
}

//*mode switching functions
function switchMode(mode) {
  const basicKeys = document.getElementById("basicKeys");
  const scientificKeys = document.getElementById("scientificKeys");
  const basicBtn = document.getElementById("basicModeBtn");
  const scientificBtn = document.getElementById("scientificModeBtn");

  if (mode === "basic") {
    basicKeys.classList.add("active");
    scientificKeys.classList.remove("active");
    basicBtn.classList.add("active");
    scientificBtn.classList.remove("active");
  } else {
    basicKeys.classList.remove("active");
    scientificKeys.classList.add("active");
    basicBtn.classList.remove("active");
    scientificBtn.classList.add("active");
  }

  clearDisplay();
}

//*simple mathematical functions (trig, log, etc.)
function calculateSimpleFunction(func) {
  try {
    let value = display.value;

    value = value.replace(/pi/g, Math.PI).replace(/e/g, Math.E);

    //* evaluation on numbers
    if (!value.includes("x")) {
      let result;
      const num = eval(value);

      switch (func) {
        case "sqrt":
          if (num < 0) {
            throw new Error("Cannot take square root of negative number");
          }
          result = Math.sqrt(num);
          break;
        case "sin":
          result = Math.sin(num);
          break;
        case "cos":
          result = Math.cos(num);
          break;
        case "tan":
          result = Math.tan(num);
          break;
        case "log":
          if (num <= 0) {
            throw new Error("Cannot take logarithm of non-positive number");
          }
          result = Math.log10(num);
          break;
        case "ln":
          if (num <= 0) {
            throw new Error(
              "Cannot take natural logarithm of non-positive number"
            );
          }
          result = Math.log(num);
          break;
        default:
          throw new Error("Unknown function");
      }

      display.value = result;
    } else {
      //*for expressions with variables we will go to Flask backend
      let expression;

      switch (func) {
        case "sqrt":
          expression = `sqrt(${value})`;
          break;
        case "sin":
          expression = `sin(${value})`;
          break;
        case "cos":
          expression = `cos(${value})`;
          break;
        case "tan":
          expression = `tan(${value})`;
          break;
        case "log":
          expression = `log(${value}, 10)`;
          break;
        case "ln":
          expression = `log(${value})`;
          break;
        default:
          throw new Error("Unknown function");
      }

      //*send to backend for processing
      fetch("api/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          expression: expression,
          operation: "function",
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            display.value = `Error: ${data.error}`;
          } else {
            display.value = data.result;
          }
        })
        .catch((error) => {
          display.value = "Error: " + error.message;
          console.error("Error:", error);
        });
    }
  } catch (error) {
    display.value = `Error: ${error.message}`;
  }
}

//! scientific calculator functions
function calculateScientific(operation) {
  const expression = display.value;

  //*for eq operation checking if the user enters =
  if (operation === "solve" && !expression.includes("=")) {
    alert("For equation solving, use format like 'x^2-4=0'");
    return;
  }

  //* flask will handle it :)
  fetch("/api/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      expression: expression,
      operation: operation,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        display.value = `Error: ${data.error}`;
      } else {
        if (Array.isArray(data.result)) {
          //* For multiple solutions (like when solving equations)
          display.value = `Solutions: ${data.result.join(", ")}`;
        } else {
          display.value = data.result;
        }
      }
    })
    .catch((error) => {
      display.value = "Error: " + error.message;
      console.error("Error:", error);
    });
}

//! limit calculation
function showLimitInput() {
  //*checking the existent of the expression
  if (!display.value) {
    alert("Enter an expression before calculating its limit");
    return;
  }

  limitModal.style.display = "block";
}

function closeModal() {
  limitModal.style.display = "none";
}

function calculateLimit() {
  const expression = display.value;
  const xValue = document.getElementById("limitValue").value;

  if (!xValue) {
    alert("Please enter a limit value");
    return;
  }

  //*send the limit calculation request
  fetch("/api/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      expression: expression,
      operation: "limit",
      x_value: xValue,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        display.value = `Error: ${data.error}`;
      } else {
        display.value = `Limit: ${data.result}`;
      }
      closeModal();
    })
    .catch((error) => {
      display.value = "Error: " + error.message;
      console.error("Error:", error);
      closeModal();
    });
}

//*close the limit  modal when clicking outside of it
window.onclick = function (event) {
  if (event.target == limitModal) {
    closeModal();
  }
};
