const express = require("express");
const multer = require("multer");
const app = express();
app.use(express.json());

// Set up multer for file uploads
const storage = multer.memoryStorage(); // Store files in memory
const upload = multer({ storage: storage });

// Route for uploading songs
app.post("/upload", upload.single("song"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded" });
  }

  // Here you would process the file with your AI model
  // For example, change the style of the song
  // const processedSong = await changeSongStyle(req.file.buffer);

  res.json({
    message: "Song uploaded successfully",
    file: req.file.originalname,
  });
});

app.get("/", (req, res) => {
  res.send("AI Music Transfer API");

  // 404 PAGE
  app.get("*", (req, res) => {
    res.json({ error: "Page not found" });
  });
});

module.exports = app;
