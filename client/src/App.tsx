// MyForm.tsx
import React, { useState, ChangeEvent, FormEvent } from "react";
import "./App.css"; // Import the CSS file
import axios from "axios";
import Card from "./Card";
import Card2 from "./Card2";

type udemyDataType = {
  course_title: string;
  is_paid: string;
  level: string;
  price: string;
  url: string;
};

type courseraDataType = {
  course_difficulty: string;
  course_organization: string;
  course_rating: number;
  course_students_enrolled: string;
  course_title: string;
};

type Data = {
  udemyData: udemyDataType[];
  courseraData: courseraDataType[];
};
interface FormData {
  topic: string;
  skillLevel: "beginner" | "intermediate" | "advanced";
}

const MyForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    topic: "",
    skillLevel: "beginner",
  });
  const [data, setData] = useState<null | Data>(null);
  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    enum SkillLevelForUdemy {
      beginner = "Beginner-Level",
      intermediate = "Intermediate-Level",
      advanced = "Expert-Level",
    }
    enum SkillLevelForCoursera {
      beginner = "Beginner",
      intermediate = "Intermediate",
      advanced = "Advanced",
    }
    const urludemy = `http://localhost:8001/udemy/${formData.topic}/${
      SkillLevelForUdemy[formData.skillLevel]
    }`;
    const urlcoursera = `http://localhost:8001/coursera/${formData.topic}/${
      SkillLevelForCoursera[formData.skillLevel]
    }`;

    axios
      .get(urludemy)
      .then((res) => {
        console.log(res.data);
        setData((prevData) => ({
          udemyData: res.data.data,
          courseraData: prevData ? prevData.courseraData : [],
        }));
      })
      .catch((err) => {
        console.log(err);
      });
    axios
      .get(urlcoursera)
      .then((res) => {
        console.log(res.data);
        setData((prevData) => ({
          udemyData: prevData ? prevData.udemyData : [],
          courseraData: res.data.data,
        }));
      })
      .catch((err) => {
        console.log(err);
      });
  };

  console.log(data);
  return (
    <div>
      {data ? (
        <div className="course">
          <h1>Udemy</h1>
          <div className="courses">
            {(data.udemyData && data.udemyData.length) > 0 ? (
              data.udemyData.map((course, index) => (
                <Card key={index} courseData={course} />
              ))
            ) : (
              <h1>No data in Dataset</h1>
            )}
          </div>
          <h1>Coursera</h1>
          <div className="courses">
            {data.courseraData && data.courseraData.length > 0 ? (
              data.courseraData.map((course, index) => (
                <Card2 key={index} courseData={course} />
              ))
            ) : (
              <h1>No data in Dataset</h1>
            )}
          </div>
        </div>
      ) : (
        <div className="form">
          <form onSubmit={handleSubmit} className="my-form">
            <div className="input-group">
              <label htmlFor="topic" className="label">
                Topic:
              </label>
              <input
                type="text"
                id="topic"
                name="topic"
                value={formData.topic}
                onChange={handleInputChange}
                className="input"
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="skillLevel" className="label">
                Skill Level:
              </label>
              <select
                id="skillLevel"
                name="skillLevel"
                value={formData.skillLevel}
                onChange={handleInputChange}
                className="select"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <button type="submit" className="button">
              Submit
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default MyForm;
