import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import tw from 'twin.macro';
import { useSwipeable } from 'react-swipeable';

const Container = tw.div``;
const MediaBox = tw.div``;
const MetaInfo = tw.div``;

function Swipe() {

    const [startTime, setStartTime] = useState(null);
    const [duration, setDuration] = useState(null);


    // Function to handle swipe
    const handleSwipe = (eventData) => {
        if (eventData.dir === 'Left') {
            // Mimic button press for "No" button
            document.getElementById('noButton').click();

        } else if (eventData.dir === 'Right') {
            // Handle swipe right (like)
            document.getElementById('yesButton').click();
        }
    };

    // Function to handle button click
    const handleNoButtonClick = () => {
        console.log(' NO Button clicked');
        // Add logic here for opening link
    };

    const handleYesButtonClick = () => {
        console.log(' YES Button clicked');
        // Add logic here for opening link
    };

    // Create a swipeable component using useSwipeable hook
    const swipeHandlers = useSwipeable({
        onSwiped: handleSwipe
    });

    return (
        <Container {...swipeHandlers}>
            <MediaBox>
                <h1>Image</h1>
            </MediaBox>

            <MetaInfo>
                <h2>Meta Info</h2>
                <h2>Price</h2>
            </MetaInfo>

            <Link to="/">
                <button id="noButton" onClick={handleNoButtonClick}>No</button>
            </Link>
            <Link to="/">
                <button id="yesButton" onClick={handleYesButtonClick}>Yes</button>
            </Link>
        </Container>
    );
}


export default Swipe;


//Hmmmm, when the screen gets smaller, i need the image to become larger than the meta text. save for later