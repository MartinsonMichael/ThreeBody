import * as React from 'react';

export interface CounterProps {
    count: number
}

export interface CounterState {
    count: number
}

export class Counter extends React.Component<CounterProps, CounterState> {
    // static defaultProps: CounterProps = {
    //     count: 10
    // };

    constructor(props: CounterProps) {
        super(props);
        this.state = {
            count: props.count,
        }
    }

    increment = () => {
        this.setState({count: this.state.count + 1});
    };

    decrement = () => {
        this.setState({count: this.state.count - 1});
    };

    render () {
        return (
            <div style={{"display": "flex"}}>
                <button onClick={ this.decrement }> - </button>
                <h1> { this.state.count } </h1>
                <button onClick={ this.increment }> + </button>
            </div>
        );
    }
}