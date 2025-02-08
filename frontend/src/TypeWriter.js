import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const Typewriter = ({ text, speed = 200 }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (!text || index >= text.length) return;

    const intervalId = setInterval(() => {
      setDisplayedText((prev) => prev + text[index]);
      setIndex((prevIndex) => prevIndex + 1);
    }, speed);

    return () => clearInterval(intervalId);
  }, [text, index, speed]);

  return <ReactMarkdown>{displayedText}</ReactMarkdown>;
};

export default Typewriter;