import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "./../UserContext.js";
import Load from "./../images/Load.png";
import "./../styles/Signup.css";

function Signup() {
  const user = useContext(UserContext);
  const navigate = useNavigate();

  if (user.username != null) {
    return (
      <img
        src={Load}
        alt=""
        onLoad={() => {
          navigate("/");
        }}
      />
    );
  } else {
    return (
      <div id="signup-content">
        <form id="signup-form">
          <h2 id="signup-header">Sign Up</h2>
          <br />
          <label for="username">Username:</label>
          <br />
          <input class="signup-input" type="text" name="username" />
          <br />
          <br />
          <label for="password">Password:</label>
          <br />
          <input class="signup-input" type="password" name="password" />
          <br />
          <p id="signup-login">
            Have an account?{" "}
            <span
              id="signup-login-link"
              onClick={() => {
                navigate("/login");
              }}
            >
              Log In
            </span>
          </p>
          <input
            id="signup-submit"
            type="button"
            value="Submit"
            onClick={() => {
              // verify validity of username and password
              // create user entry in database
              // set logged in username
              // redirect to home
            }}
          />
        </form>
      </div>
    );
  }
}

export default Signup;
