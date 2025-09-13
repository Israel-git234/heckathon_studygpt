import React, { useState } from 'react';
import './QuizComponent.css';

const QuizComponent = ({ quiz, onComplete }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  if (!quiz || quiz.length === 0) {
    return (
      <div className="quiz-container">
        <p>No quiz questions available for this concept.</p>
      </div>
    );
  }

  const handleAnswerSelect = (questionIndex, answerIndex) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionIndex]: answerIndex
    }));
  };

  const handleSubmitQuiz = () => {
    let correctAnswers = 0;
    
    quiz.forEach((question, index) => {
      if (selectedAnswers[index] === question.correct) {
        correctAnswers++;
      }
    });

    setScore(correctAnswers);
    setShowResults(true);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < quiz.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      handleSubmitQuiz();
    }
  };

  const handleRestart = () => {
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
    setScore(0);
  };

  const currentQ = quiz[currentQuestion];
  const isAnswered = selectedAnswers[currentQuestion] !== undefined;

  if (showResults) {
    const percentage = Math.round((score / quiz.length) * 100);
    
    return (
      <div className="quiz-container results">
        <div className="quiz-header">
          <h3>🎯 Quiz Results</h3>
        </div>
        
        <div className="score-display">
          <div className="score-circle">
            <span className="score-number">{score}</span>
            <span className="score-total">/{quiz.length}</span>
          </div>
          <div className="score-percentage">{percentage}%</div>
          <div className="score-message">
            {percentage >= 80 ? '🎉 Excellent!' : 
             percentage >= 60 ? '👍 Good job!' : 
             '📚 Keep studying!'}
          </div>
        </div>

        <div className="question-results">
          {quiz.map((question, index) => {
            const userAnswer = selectedAnswers[index];
            const isCorrect = userAnswer === question.correct;
            
            return (
              <div key={index} className={`question-result ${isCorrect ? 'correct' : 'incorrect'}`}>
                <div className="question-text">{question.question}</div>
                <div className="answer-feedback">
                  <div className="user-answer">
                    Your answer: {question.options[userAnswer] || 'Not answered'}
                  </div>
                  {!isCorrect && (
                    <div className="correct-answer">
                      Correct answer: {question.options[question.correct]}
                    </div>
                  )}
                  <div className="explanation">{question.explanation}</div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="quiz-actions">
          <button className="btn btn-secondary" onClick={handleRestart}>
            Retake Quiz
          </button>
          <button className="btn btn-primary" onClick={onComplete}>
            Continue Learning
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h3>🧠 Test Your Knowledge</h3>
        <div className="question-counter">
          Question {currentQuestion + 1} of {quiz.length}
        </div>
      </div>

      <div className="question-container">
        <div className="question-text">
          {currentQ.question}
        </div>

        <div className="options-container">
          {currentQ.options.map((option, index) => (
            <label 
              key={index} 
              className={`option-label ${selectedAnswers[currentQuestion] === index ? 'selected' : ''}`}
            >
              <input
                type="radio"
                name={`question-${currentQuestion}`}
                value={index}
                checked={selectedAnswers[currentQuestion] === index}
                onChange={() => handleAnswerSelect(currentQuestion, index)}
              />
              <span className="option-text">{option}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="quiz-actions">
        <button 
          className="btn btn-primary"
          onClick={handleNextQuestion}
          disabled={!isAnswered}
        >
          {currentQuestion === quiz.length - 1 ? 'Submit Quiz' : 'Next Question'}
        </button>
      </div>
    </div>
  );
};

export default QuizComponent;
