// ISSUE 1: Unexpected string concatenation (prefer-template)
const userName = 'John';
const message = 'Welcome ' + userName + '!';
const errorMsg = 'Error: ' + error.code + ' - ' + error.message;

// ISSUE 2: Use object destructuring (prefer-destructuring)
const user = { name: 'Alice', age: 30 };
const name = user.name;
const age = user.age;

// ISSUE 3: Variable never reassigned, use 'const' instead (prefer-const)
let period = '2024-Q1';
let config = { apiUrl: 'https://api.example.com' };

// ISSUE 4: Unary operator '++' used (no-plusplus)
let counter = 0;
counter++;
for (let i = 0; i < 10; i++) {
  console.log(i);
}

// ISSUE 5: Unexpected var, use let or const instead (no-var)
var oldVariable = 'legacy code';
var globalConfig = {};

// ISSUE 6: Unnecessary 'else' after 'return' (no-else-return)
function validateAge(age) {
  if (age >= 18) {
    return true;
  } else {
    return false;
  }
}

function getStatus(value) {
  if (value > 100) {
    return 'high';
  } else {
    return 'low';
  }
}

// ISSUE 7: Use Boolean() instead of !! (no-implicit-coercion)
const hasDescription = !!infoBox.description;
const isValid = !!userInput;
