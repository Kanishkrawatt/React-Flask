import React from "react";
import "./card.css";

interface ServerData {
  course_title: string;
  is_paid: string;
  level: string;
  price: string;
  url: string;
}

interface CardComponentProps {
  courseData: ServerData;
}

const CardComponent: React.FC<CardComponentProps> = ({ courseData }) => {
  const { course_title, is_paid, level, price, url } = courseData;

  return (
    <div className="card">
      <div className="card-content">
        <h2 className="card-title">
          <a href={url} target="_blank" rel="noopener noreferrer">
            {course_title}
          </a>
        </h2>
        <p className="card-text">Level: {level}</p>
        <p className="card-text">Paid: {is_paid}</p>
        <p className="card-text">Price: {price}</p>
      </div>
    </div>
  );
};

export default CardComponent;
