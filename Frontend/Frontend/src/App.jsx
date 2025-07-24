import React, { useState } from "react";
import axios from "axios";
<<<<<<< HEAD
=======
import PhoneInput from "react-phone-input-2";
import "react-phone-input-2/lib/style.css";
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
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

<<<<<<< HEAD
const labels = ["Strongly Disagree", "Disagree", "Maybe", "Agree", "Strongly Agree"];
const values = { "Strongly Disagree": 1, "Disagree": 2, "Maybe": 3, "Agree": 4, "Strongly Agree": 5 };

function App() {
  const [step, setStep] = useState(1);
  const [score, setScore] = useState(0);
=======
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
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    contact: "",
    responses: {}
  });
<<<<<<< HEAD
=======
  const [score, setScore] = useState(0);
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f

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
<<<<<<< HEAD
    const answers = Object.values(form.responses).map(Number);
    const total = answers.reduce((a, b) => a + b, 0);
    const percent = Math.round((total / 60) * 100);
    setScore(percent);

    if (!form.name || !form.email || !form.company || !form.contact) {
      alert("❗ Please fill out all fields including contact number.");
      return;
    }
=======
    const valuesList = Object.values(form.responses).map((val) => Number(val));
    const totalScore = valuesList.reduce((a, b) => a + b, 0);
    const percentScore = Math.round((totalScore / 60) * 100);
    setScore(percentScore);
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f

    if (!validateEmail(form.email)) {
      alert("❌ Please use a valid *organization email* (not Gmail, Yahoo, etc).");
      return;
    }

<<<<<<< HEAD
    if (answers.length < 12) {
      alert("❗ Please answer all 12 questions.");
=======
    if (!form.contact || form.contact.length < 6) {
      alert("❗ Please enter a valid contact number.");
      return;
    }

    if (valuesList.length < 12) {
      alert("❗ Please answer all questions.");
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
      return;
    }

    try {
      await axios.post("https://brand-health-assessment-app-backend.onrender.com/submit", form);
<<<<<<< HEAD
      setStep(3);
    } catch (err) {
      console.error(err);
      alert("❌ Submission failed. Please try again later.");
=======
      setStep(3); // Show thank-you page
    } catch (err) {
      console.error(err);
      alert("❌ Submission failed: Could not reach backend.");
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
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

          <label>Contact Number</label>
<<<<<<< HEAD
          <input name="contact" onChange={handleInputChange} placeholder="+91XXXXXXXXXX" />
=======
          <PhoneInput
            country={'in'}
            value={form.contact}
            onChange={(phone) => setForm({ ...form, contact: phone })}
            inputProps={{
              name: 'phone',
              required: true,
              autoFocus: false
            }}
          />
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f

          <button
            className="next-btn"
            onClick={() => {
              if (!validateEmail(form.email)) {
<<<<<<< HEAD
                alert("❌ Only organization emails are accepted.");
=======
                alert("❌ Only organizational emails are accepted (not Gmail/Yahoo).");
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
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
        <div className="thank-you-page">
          <div className="thank-you-card fancy-border">
            <h2>🎉 Thank You!</h2>
<<<<<<< HEAD
            <p className="highlight">Your Brand Health Assessment has been submitted.</p>
            <p>✅ <strong>Your Brand Health Score is :</strong> <span className="score">{score}%</span></p>
            <p>📩 A detailed PDF report has been sent to: <strong>{form.email}</strong></p>
            <p>📱 Also sent to WhatsApp: <strong>{form.contact}</strong></p>
            <p className="footer-note">We appreciate your time. Stay brand-strong!</p>
=======
            <p className="highlight">Your Brand Health Assessment has been submitted successfully.</p>
            <p>✅ <strong>Score:</strong> <span className="score">{score}%</span></p>
            <p>📩 A detailed PDF report has been emailed to: <strong>{form.email}</strong></p>
            <p>📱 A copy has also been sent to your WhatsApp: <strong>{form.contact}</strong></p>
            <p className="footer-note">We appreciate your time. Your insights help shape a stronger brand identity!</p>
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
