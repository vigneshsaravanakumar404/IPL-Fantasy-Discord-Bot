import Unknown from './../images/Unknown.png';
import './../styles/Players.css';

function Player(props) {
    var image = "https://scores.iplt20.com/ipl/playerimages/" + props.name.replaceAll(' ', '%20') + '.png';

    const check = new Image();
    check.src = image;
    if(!check.complete)
    {
        image = Unknown;
    }

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

function Players() {
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

export default Players;