"use strict";

let time = 5000;
const place = document.querySelector(".timer");
const data = document.querySelector(".data").textContent;
const d = JSON.parse(data);
console.log(place, d);

const displayTime = function () {
  let current_time = time;
  const hrs = String(Math.floor(current_time / (60 * 60))).padStart(2, "0");
  current_time %= 60 * 60;
  const mins = String(Math.floor(current_time / 60)).padStart(2, "0");
  current_time %= 60;
  const secs = String(current_time).padStart(2, "0");
  const value = `${hrs}:${mins}:${secs}`;
  place.textContent = value;
  time -= 1;
};

const timer = async function () {
  setInterval(function () {
    displayTime();
  }, 1000);
};

timer();
