import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const questions = [
  "My company's product or service has a strong and clear point of differentiation from my competitors.",
  "My client and I can summarize my brand in one word/statement.",
  "The value of my product or services is relevant to the current market environment.",
  "There is harmony/linkage between my company's vision, mission, values and strategy.",
  "My employees are brand ambassadors of the company and can articulate how the offering differs from competitors.",
  "I regularly survey my customers on my brand and use their feedback as an input for strategy.",
  "My marketing material clearly communicates the company's brand.",
  "Management reinforces the company's brand in all staff meetings and employee interactions.",
  "All departments follow the company's brand guidelines document and prescribed templates.",
  "Clients get the same positive brand experience no matter which department or employee they interact with.",
  "My company has a robust mechanism to deliver a brand experience at every stage of the customer journey (attract, engage, and retain).",
  "My clients do not switch between my competitors and me and regularly refer others to my company."
];

const labels = [
  "Strongly Disagree",
  "Disagree",
  "Maybe",
  "Agree",
  "Strongly Agree"
];

const values = {
  "Strongly Disagree": 1,
  "Disagree": 2,
  "Maybe": 3,
  "Agree": 4,
  "Strongly Agree": 5
};

function App() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ name: "", email: "", company: "", responses: {} });
  const [score, setScore] = useState(0);

  const handleInputChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRadioChange = (q, val) => {
    setForm({ ...form, responses: { ...form.responses, [q]: val } });
  };

  const validateEmail = (email) => {
    const domain = email.split("@")[1];
    const publicDomains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"];
    return domain && !publicDomains.includes(domain);
  };

  const handleSubmit = async () => {
    const valuesList = Object.values(form.responses).map((val) => Number(val));
    const totalScore = valuesList.reduce((a, b) => a + b, 0);
    const percentScore = Math.round((totalScore / 60) * 100);
    setScore(percentScore);

    if (!validateEmail(form.email)) {
      alert("❌ Please use a valid *organization email* (not Gmail, Yahoo, etc).");
      return;
    }

    if (valuesList.length < 12) {
      alert("❗ Please answer all questions.");
      return;
    }

    try {
      await axios.post("https://brand-health-assessment-app-backend.onrender.com/submit", form);
      setStep(3); // Show thank-you page
    } catch (err) {
      console.error(err);
      alert("❌ Submission failed: Could not reach backend.");
    }
  };

  return (
    <div className="container">
      {step === 1 && (
        <div className="form-card">
          <h2>Brand Health Assessment</h2>
          <label>Name</label>
          <input name="name" onChange={handleInputChange} placeholder="Your Name" />

          <label>Company Email</label>
          <input name="email" onChange={handleInputChange} placeholder="you@company.com" />

          <label>Company Name</label>
          <input name="company" onChange={handleInputChange} placeholder="Company Name" />

          <button
            className="next-btn"
            onClick={() => {
              if (!validateEmail(form.email)) {
                alert("❌ Only organizational emails are accepted (not Gmail/Yahoo).");
              } else {
                setStep(2);
              }
            }}
          >
            Next
          </button>
        </div>
      )}

      {step === 2 && (
        <div className="form-card">
          <h2>Answer All Questions</h2>
          {questions.map((q, i) => (
            <div key={i} className="question-block">
              <p>{q}</p>
              {labels.map((label, idx) => (
                <label key={idx} className="radio-label">
                  <input
                    type="radio"
                    name={`q${i}`}
                    value={values[label]}
                    onChange={() => handleRadioChange(q, values[label])}
                  />{" "}
                  {label}
                </label>
              ))}
            </div>
          ))}
          <button className="submit-btn" onClick={handleSubmit}>
            Submit
          </button>
        </div>
      )}

      {step === 3 && (
        <div className="thank-you-card">
          <h2>✅ Thank you for your submission!</h2>
          <p>📊 Your brand health score is: <strong>{score}%</strong></p>
          <p>📩 A detailed report has been sent to: <strong>{form.email}</strong></p>
        </div>
      )}
    </div>
  );
}

export default App;
