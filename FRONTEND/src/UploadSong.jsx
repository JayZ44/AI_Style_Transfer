// Example React component for uploading a song
import React, { useState } from "react";
import axios from "axios";

const UploadSong = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("song", file);

    try {
      const response = await axios.post("/upload", formData);
      console.log(response.data);
    } catch (error) {
      console.error("Error uploading song:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleFileChange} accept="audio/*" />
      <button type="submit">Upload Song</button>
    </form>
  );
};

export default UploadSong;
