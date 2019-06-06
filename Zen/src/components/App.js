// Dependencies
import React, { Component, Redirect } from 'react';
import { Route, Switch } from 'react-router-dom';

// Components
import Login from './User/Login';
import Transfer from './Transfer';
import Password from './User/Password';
import Panel from './Panel';
import Welcome from './Welcome';
import Page404 from './Errors/404';


class App extends Component {

  constructor(props) {
    super(props);
    let userId = '';
    let authenticated = false;
    if (typeof(Storage) !== 'undefined') {
      userId = localStorage.getItem('ZenCoinUserId');
      authenticated = (localStorage.getItem('ZenCoinAuthenticated') === 'true');
    }
    this.state = {
      authenticated: authenticated,
      userId: userId
    }
  }

  authenticate = (userId=null) => {
    if (typeof(Storage) !== 'undefined') {
      localStorage.setItem('ZenCoinUserId', userId);
      localStorage.setItem('ZenCoinAuthenticated', userId ? true : false);
    }
    this.setState({
      authenticated: !this.state.authenticated,
      userId: userId
    });
  }

  render () {
    return (
      <Switch>
        <Route exact path="/" component={() => <Welcome auth={this.state.authenticated} />} />
        <Route exact path="/login" component={() => <Login authMethod={this.authenticate} auth={this.state.authenticated} />} />
        <Route
          exact
          path="/panel"
          component={
            () => this.state.authenticated
              ? <Panel authMethod={this.authenticate} auth={this.state.authenticated} />
              : <Login authMethod={this.authenticate} auth={this.state.authenticated} />
            } />
        <Route
          exact
          path="/transfer"
          component={
            () => this.state.authenticated
              ? <Transfer authMethod={this.authenticate} auth={this.state.authenticated} />
              : <Login authMethod={this.authenticate} auth={this.state.authenticated} />
            } />
        <Route
          exact
          path="/password"
          component={
            () => this.state.authenticated
              ? <Password authMethod={this.authenticate} auth={this.state.authenticated} />
              : <Login authMethod={this.authenticate} auth={this.state.authenticated} />
            } />
        <Route component={() => <Page404 />} />
      </Switch>
    );
  }

}

export default App;