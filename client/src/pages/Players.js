import { useState } from 'react';
import Unknown from './../images/Unknown.png';
import './../styles/Players.css';

function Player(props) {
    const [image, setImage] = useState(Unknown);

    const check = new Image();
    check.src = "https://scores.iplt20.com/ipl/playerimages/" + props.name.replaceAll(' ', '%20') + '.png';
    check.onload = () => {
        setImage(check.src);
    };

    return(
        <div class='player-body'>
            <div class='player-rank-body'>
                <p class='player-rank'>1</p>
            </div>
            <img class='player-image' src={image} alt=''/>
            <p class='player-name'>{props.name}</p>
            <p class='player-points'>{props.points}</p>
        </div>
    );
}

function MobilePlayer(props)
{
    return(
        <div class='player-body'>
            <div class='player-rank-body-mobile'>
                <p class='player-rank-mobile'>1</p>
            </div>
            <p class='player-name-mobile'>{props.name}</p>
            <p class='player-points-mobile'>{props.points}</p>
        </div>
    );
}

function Players() {
    const [width, setWidth] = useState(window.screen.width);

    window.addEventListener('resize', function(event) {
        setWidth(window.screen.width)
    }, true);

    if(width <= 768)
    {
        return(
            <div id='players-content'>
                <h1>Player Rankings</h1>
                <MobilePlayer name={'Virat Kohli'} points={1231}/>
                <MobilePlayer name={'Faf Du Plessis'} points={1012}/>
                <MobilePlayer name={'Glenn Maxwell'} points={954}/>
                <MobilePlayer name={'Mohammed Siraj'} points={912}/>
            </div>
        );
    }
    else
    {
        return(
            <div id='players-content'>
                <h1>Player Rankings</h1>
                <Player name={'Virat Kohli'} points={1231}/>
                <Player name={'Faf Du Plessis'} points={1012}/>
                <Player name={'Glenn Maxwell'} points={954}/>
                <Player name={'Mohammed Siraj'} points={912}/>
            </div>
        );
    }
}

export default Players;