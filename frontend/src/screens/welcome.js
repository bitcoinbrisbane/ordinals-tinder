import React from "react";
import { Link } from "react-router-dom";
import tw from "twin.macro";

const Container = tw.div`flex flex-col h-screen w-full items-center justify-center bg-gray-100`;
const Heading = tw.h1`text-2xl font-bold`;
const Button = tw.button`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded`;

function Welcome() {
    return (
        <Container>
            <Heading>Welcome</Heading>
            <Link to = "/swipe"> <Button>Connect wallet</Button> </Link>
        </Container>
    );
}

export default Welcome;



//Connect to anduro wallet