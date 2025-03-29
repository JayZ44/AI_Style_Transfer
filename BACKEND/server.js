// DEPENDENCIES
const app = require("./index.js");

// CONFIGURATION
require("dotenv").config();
const PORT = process.env.PORT || 3004;

// LISTEN
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
