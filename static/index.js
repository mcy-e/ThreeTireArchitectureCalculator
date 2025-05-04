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

//* Authentication JavaScript for the calculator app

//* check authentication status when page loads
document.addEventListener('DOMContentLoaded', function() {
  checkAuthStatus();
});

//* toggle between login and register forms
function toggleAuthForms() {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  
  loginForm.classList.toggle('hidden');
  registerForm.classList.toggle('hidden');
  
  document.getElementById('login-message').textContent = '';
  document.getElementById('register-message').textContent = '';
}

function checkAuthStatus() {
  fetch('/api/authentication/check')
      .then(response => response.json())
      .then(data => {
          if (data.authenticated) {
              showMainInterface(data.username);
          }
      })
      .catch(error => {
          console.error('Error checking authentication:', error);
      });
}

function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;
  const messageElement = document.getElementById('login-message');
  
  if (!username || !password) {
      messageElement.textContent = 'Please enter both username and password';
      messageElement.classList.add('error');
      return;
  }
  
  fetch('/api/authentication/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          username: username,
          password: password
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          messageElement.textContent = data.message;
          messageElement.classList.remove('error');
          messageElement.classList.add('success');
          
          setTimeout(() => {
              showMainInterface(username);
          }, 1000);
      } else {
          messageElement.textContent = data.message;
          messageElement.classList.add('error');
          messageElement.classList.remove('success');
      }
  })
  .catch(error => {
      messageElement.textContent = 'An error occurred. Please try again.';
      messageElement.classList.add('error');
      console.error('Error:', error);
  });
}

//*sign up (register the new users)
function register() {
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;
  const confirmPassword = document.getElementById('register-confirm').value;
  const messageElement = document.getElementById('register-message');
  
  if (!username || !password || !confirmPassword) {
      messageElement.textContent = 'Please fill in all fields';
      messageElement.classList.add('error');
      return;
  }
  
  if (password !== confirmPassword) {
      messageElement.textContent = 'Passwords do not match';
      messageElement.classList.add('error');
      return;
  }
  
  fetch('/api/authentication/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          username: username,
          password: password
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          messageElement.textContent = data.message;
          messageElement.classList.remove('error');
          messageElement.classList.add('success');
          
          //*switch to login form after successful registration
          setTimeout(() => {
              toggleAuthForms();
              document.getElementById('login-username').value = username;
              document.getElementById('login-message').textContent = 'Registration successful! Please log in.';
              document.getElementById('login-message').classList.add('success');
          }, 1500);
      } else {
          messageElement.textContent = data.message;
          messageElement.classList.add('error');
          messageElement.classList.remove('success');
      }
  })
  .catch(error => {
      messageElement.textContent = 'An error occurred. Please try again.';
      messageElement.classList.add('error');
      console.error('Error:', error);
  });
}

//*main calculator interface
function showMainInterface(username) {
  document.getElementById('auth-container').classList.add('hidden');
  document.getElementById('main-container').classList.remove('hidden');
  document.getElementById('welcome-message').textContent = `Welcome, ${username}!`;
  
  //*display user's calculation history
  fetchHistory();
}

//*logout
function logout() {
  fetch('/api/authentication/logout', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          
          document.getElementById('auth-container').classList.remove('hidden');
          document.getElementById('main-container').classList.add('hidden');
          
          //*clear login form fields
          document.getElementById('login-username').value = '';
          document.getElementById('login-password').value = '';
          document.getElementById('login-message').textContent = '';
          
          //*hide  panel if it's open
          document.getElementById('history-panel').classList.add('hidden');
      }
  })
  .catch(error => {
      console.error('Error during logout:', error);
  });
}

//*history panel visibility
function toggleHistory() {
  const historyPanel = document.getElementById('history-panel');
  historyPanel.classList.toggle('hidden');
  
  if (!historyPanel.classList.contains('hidden')) {
      fetchHistory();
  }
}

//*user's calculation history
function fetchHistory() {
  fetch('/api/authentication/history')
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          const historyList = document.getElementById('history-list');
          historyList.innerHTML = '';
          
          if (data.history && data.history.length > 0) {
              data.history.forEach(item => {
                  const listItem = document.createElement('li');
                  listItem.className = 'history-item';
                  
                  // Format the history item based on operation type
                  let displayText = '';
                  
                  switch (item.operation) {
                      case 'derivative':
                          displayText = `d/dx(${item.expression}) = ${item.result}`;
                          break;
                      case 'integral':
                          displayText = `∫(${item.expression})dx = ${item.result}`;
                          break;
                      case 'limit':
                          displayText = `lim(${item.expression}) = ${item.result}`;
                          break;
                      case 'solve':
                          displayText = `${item.expression}: ${item.result}`;
                          break;
                      case 'function':
                          displayText = `f(${item.expression}) = ${item.result}`;
                          break;
                      default:
                          displayText = `${item.expression} = ${item.result}`;
                  }
                  
                  listItem.textContent = displayText;
                  
                  // Add click handler to load calculation back to display
                  listItem.addEventListener('click', function() {
                      document.getElementById('display').value = item.expression;
                      document.getElementById('history-panel').classList.add('hidden');
                  });
                  
                  historyList.appendChild(listItem);
              });
          } else {
              const emptyItem = document.createElement('li');
              emptyItem.textContent = 'No calculation history available';
              historyList.appendChild(emptyItem);
          }
      })
      .catch(error => {
          console.error('Error fetching history:', error);
          const historyList = document.getElementById('history-list');
          historyList.innerHTML = '<li>Error loading history</li>';
      });
}