import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import tw from 'twin.macro';
import { useSwipeable } from 'react-swipeable';

import { ReactComponent as Up } from "../images/up.svg";
import { ReactComponent as Down } from "../images/down.svg";
import { ReactComponent as Purchase } from "../images/purchase.svg";

const Container = tw.div`bg-[#292929] h-screen w-screen mx-auto flex flex-col justify-center items-center pb-5`;
const MediaBox = tw.div`relative bg-[#000000] rounded-[20px] h-[70%] w-[90%] mx-auto mt-5 bg-cover bg-center overflow-hidden`;

const ThumbnailPlaceholder = tw.div`absolute top-4 right-4 w-[125px] h-[125px] bg-black`;

const MetaInfo = tw.div`justify-center mx-auto text-center z-10 absolute bottom-5 left-0 right-0 p-4 text-white cursor-pointer`;
const Title = tw.h1`text-[48px] font-bold`;
const Price = tw.h1`text-[36px] font-bold`;

const DescriptionContainer = tw.div`z-50 absolute bottom-0 p-5 h-full bg-[#ffffff] text-[#292929] transition-all duration-500 transform translate-y-full w-full flex flex-col items-center justify-center`;
const Description = tw.p`text-lg text-[#292929] mt-2 text-center`;

const Buttons = tw.span`flex justify-center w-[85%] gap-4 mt-5`;

const UpButton = tw.svg(Up)`w-[40px] h-[40px] z-50`;
const DownButton = tw.svg(Down)`w-[40px] h-[40px] z-50`;
const PurchaseButton = tw.svg(Purchase)`w-[50px] h-[50px] z-50`;

const ButtonNo = tw.button`bg-transparent border-[#FF6F61] hover:border-[#dd3333] duration-300 rounded-full border-[1px] p-[15px] justify-center items-center`; 
const ButtonYes = tw.button`bg-transparent border-[#93c572] hover:border-[#61b744] duration-300 rounded-full border-[1px] p-[15px] justify-center items-center`; 
const ButtonPurchase = tw.button`bg-transparent border-[#FF6F61] hover:border-[#dd3333] duration-300 rounded-[75px] border-[1px] p-[15px] px-[60px] justify-center items-center`;

function Swipe({ imageUrl, onSwipe }) {
    const [startTime, setStartTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [showDescription, setShowDescription] = useState(false);

    useEffect(() => {
        const intervalId = setInterval(() => {
            setDuration(prevDuration => prevDuration + 1); 
        }, 1000);
        
        return () => clearInterval(intervalId);
    }, []);

    const handlers = useSwipeable({
        onSwipedLeft: () => handleSwipe('left'),
        onSwipedRight: () => handleSwipe('right'),
        preventDefaultTouchmoveEvent: true,
        trackMouse: true
    });

    const handleSwipe = (direction) => {
        console.log(`GH Swiped ${direction}`);
        const endTime = new Date().getTime();
        const newDuration = (endTime - startTime); 
        setDuration(newDuration);

        if (direction === 'right') {
            document.getElementById('yesButton').click();
        } else if (direction === 'left') {
            document.getElementById('noButton').click();
        }
    };

    const toggleDescription = () => {
        setShowDescription(!showDescription);
    };

    const handleNoButtonClick = () => {
        console.log('NO Button clicked');
        console.log('Duration:', duration); 
    };

    const handleYesButtonClick = () => {
        console.log('YES Button clicked');
        console.log('Duration:', duration);
    };  

    return (
        <Container>
            <MediaBox {...handlers} style={{backgroundImage: `url(${imageUrl})`}}>
    <MetaInfo onClick={toggleDescription}>
        <Title>Art Title</Title>
        <Price>105 SAT</Price>
    </MetaInfo>

    <DescriptionContainer style={{transform: showDescription ? 'translateY(0%)' : 'translateY(100%)'}} onClick={toggleDescription}>

        <Description>
            This is the description of the art piece.
        </Description>
        <Description><b>Contract ID:</b> 0xa1111ac011d00888DD91751A4b98769862213cf5</Description>
        <Description><b>Token Standard:</b> ERC-721</Description>
        <Description><b>Chain:</b> BTC </Description>
        <Description><b>Last Updated:</b> 2020</Description>
    <ThumbnailPlaceholder /> {/* Placeholder thumbnail */}
</DescriptionContainer>
</MediaBox>

            <Buttons>
                <Link to="/">
                    <ButtonNo id='noButton' onClick={handleNoButtonClick}> 
                        <DownButton />
                    </ButtonNo>
                </Link>

                <Link to="/">
                    <ButtonPurchase>
                        <PurchaseButton />
                    </ButtonPurchase>
                </Link>

                <Link to="/">
                    <ButtonYes id='yesButton' onClick={handleYesButtonClick}> 
                        <UpButton />
                    </ButtonYes>
                </Link>


            </Buttons>
        </Container>
    );
}

export default Swipe;