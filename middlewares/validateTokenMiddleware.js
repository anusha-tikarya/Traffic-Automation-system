const axios = require("axios");

// Flask validation endpoint
const FLASK_VALIDATE_URL = "http://127.0.0.1:2999/auth/validate";

/**
 * Middleware to validate the Authorization token using Flask API
 */
const validateTokenMiddleware = async (req, res, next) => {
  const authHeader = req.headers["authorization"];

  if (!authHeader || !authHeader.trim()) {
    return res.status(401).json({ message: "Unauthorized: Authorization token is required" });
  }

  try {
    const response = await axios.post(
      FLASK_VALIDATE_URL,
      {}, // Flask API does not expect a body
      {
        headers: { Authorization: authHeader },
      }
    );

    if (response.status === 200) {
      // Token is valid, proceed to the next middleware or route handler
      return next();
    }
  } catch (err) {
    if (err.response && err.response.status === 403) {
      return res.status(403).json({ message: "Forbidden: Invalid Authorization token" });
    }
    return res.status(500).json({ message: "Validation service error", error: err.message });
  }
  next();
};

module.exports = validateTokenMiddleware;
