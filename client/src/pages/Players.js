import { useState } from "react";
import Unknown from "./../images/Unknown.png";
import "./../styles/Players.css";

function Player(props) {
  const [image, setImage] = useState(Unknown);

  const check = new Image();
  check.src =
    "https://scores.iplt20.com/ipl/playerimages/" +
    props.name.replaceAll(" ", "%20") +
    ".png";
  check.onload = () => {
    setImage(check.src);
  };

  return (
    <div class="player-body">
      <div class="player-rank-body">
        <p class="player-rank">1</p>
      </div>
      {!props.mobile && <img class="player-image" src={image} alt="" />}
      <p class="player-name">{props.name}</p>
      <p class="player-points">{props.points}</p>
    </div>
  );
}

function Players() {
  const [width, setWidth] = useState(window.screen.width);

  window.addEventListener(
    "resize",
    function (event) {
      setWidth(window.screen.width);
    },
    true
  );

  return (
    <div id="players-content">
      <h1>Player Rankings</h1>
      <Player name={"Virat Kohli"} points={1231} mobile={width <= 768} />
      <Player name={"Faf Du Plessis"} points={1012} mobile={width <= 768} />
      <Player name={"Glenn Maxwell"} points={954} mobile={width <= 768} />
      <Player name={"Mohammed Siraj"} points={912} mobile={width <= 768} />
    </div>
  );
}

export default Players;
