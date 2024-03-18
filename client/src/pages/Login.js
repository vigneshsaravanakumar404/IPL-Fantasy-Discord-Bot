import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "./../UserContext.js";
import Load from "./../images/Load.png";
import "./../styles/Login.css";

function Login() {
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
      <div id="login-content">
        <form id="login-form">
          <h2 id="login-header">Log In</h2>
          <br />
          <label for="username">Username:</label>
          <br />
          <input class="login-input" type="text" name="username" />
          <br />
          <br />
          <label for="password">Password:</label>
          <br />
          <input class="login-input" type="password" name="password" />
          <br />
          <p id="login-signup">
            Don't have an account?{" "}
            <span
              id="login-signup-link"
              onClick={() => {
                navigate("/signup");
              }}
            >
              Sign Up
            </span>
          </p>
          <input
            id="login-submit"
            type="button"
            value="Submit"
            onClick={() => {
              // verify username exists and password is correct
              // set logged in username
              // redirect to home
            }}
          />
        </form>
      </div>
    );
  }
}

export default Login;
