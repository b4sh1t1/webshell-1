import React from 'react';
import './App.scss';
import { Term } from './Term';

interface LoginData {
  token: string
}

interface AppState {
  state: State
}

enum State {
  Loading = "Loading",
  Login = "Login",
  Terminal = "Terminal",
  Closed = "Closed"
}

export class App extends React.Component<{}, AppState> {

  public state = { state: State.Loading };

  constructor(props: {}) {
    super(props);
  }
  componentDidMount() {

  }

  render() {
    return (
      <Term />
    )
  }
}
