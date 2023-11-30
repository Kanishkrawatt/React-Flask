import React from "react";
import "./card.css";

interface ServerData {
  course_difficulty: string;
  course_organization: string;
  course_rating: number;
  course_students_enrolled: string;
  course_title: string;
}

interface CardComponentProps {
  courseData: ServerData;
}

const CardComponent: React.FC<CardComponentProps> = ({ courseData }) => {
  const {
    course_title,
    course_difficulty,
    course_organization,
    course_rating,
    course_students_enrolled,
  } = courseData;
  return (
    <div className="card">
      <div className="card-content">
        <h2 className="card-title">
          <a
            href={
              "https://www.coursera.org/search?query=" +
              course_title.toLowerCase().split(" ").join("-")
            }
            target="_blank"
            rel="noopener noreferrer"
          >
            {course_title}
          </a>
        </h2>
        <p className="card-text">Organization: {course_organization}</p>
        <p className="card-text">Difficulty: {course_difficulty}</p>
        <p className="card-text">Rating: {course_rating}</p>
        <p className="card-text">
          Students Enrolled: {course_students_enrolled}
        </p>
      </div>
    </div>
  );
};

export default CardComponent;
