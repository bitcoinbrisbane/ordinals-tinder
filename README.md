# ordinals-tinder
Think ordinals, swipe left, swipe right.

## About
The interfaces for buying NFTs such as Opensea do not allow for users to explore NFTs.  Netflix, a pioneer in the streaming industry, has revolutionized the way viewers discover content through its innovative use of machine learning. This technology underpins their recommendation engine, a system that analyses vast amounts of data to suggest films, series, and documentaries tailored to individual tastes. By examining user interactions, such as what they watch, how long they watch it, and their ratings, Netflix's algorithms create a highly personalized viewing experience. The system even considers factors like the time of day and the device being used for streaming. This sophisticated approach not only enhances user satisfaction by making content discovery effortless and intuitive but also benefits Netflix by increasing viewer engagement and retention. The success of this machine learning-driven recommendation system has set a benchmark in the industry, influencing how other streaming services approach content curation.

An academic paper titled "Deep Learning for Recommender Systems: A Netflix Case Study" by Steck et al., published in AI Magazine, discusses the impact of deep learning on Netflix's recommender systems. The paper outlines the challenges and lessons learned in implementing deep learning for these systems at Netflix. It highlights that different model architectures are effective for various recommendation tasks and that significant performance improvements were only observed when numerous heterogeneous features were added to the input data. This study provides insights into how deep learning has led to substantial improvements in Netflix's recommendations, both offline and online. For more details, you can refer to the full paper [here](https://ojs.aaai.org/index.php/aimagazine/article/view/18140).

Similarly, Tinder's innovative swipe interface, which popularized the simple 'swipe right to like, swipe left to pass' concept, revolutionized the online dating experience. This intuitive design made user decisions quick and easy, significantly streamlining the process of finding potential matches. By reducing the complexity of interacting with a dating app, Tinder attracted a broad user base, becoming a cultural phenomenon. Its swipe mechanism, mimicking the natural process of selection or rejection, also added a gamified element to dating, making it more engaging and less daunting for users. This innovation not only transformed the online dating landscape but also influenced user interface design in various other applications.

## This project
This project aims to build a recommendation system to allow allow users to browse new creators that they perhaps would not discover.

We will use TensorFlow Recommenders and content based filtering / collaborative filtering to build a recommendation system for NFTs.  We will use the blockchain to obtain user profiles and use this data to train our model.

## Content filtering

### Collaborative filtering

Collaborative filtering is a technique that uses the preferences of a group of people to make recommendations to other people.  It is based on the idea that people who agree in their evaluations of certain items are likely to have similar tastes for other items.  For example, a collaborative filtering recommendation system for music might make recommendations based on the songs that a user has listened to, liked, or added to a playlist.

Our NFT 1162315496355503 may have the following dimensions:

| NFT | Cost | Scarcity | Genre | Artist |
|-----|------|----------|-------|--------|
| 1   | 0.5  | 0.5      | 0.5   | 0.5    |

We can use the following formula to calculate the distance between two NFTs:

Previous users selections can be used to calculate the distance between two NFTs.  The distance can be used to suggest the next NFT to the user.

Eg:

| User | NFT | Liked |
|------|-----|-------|
| 1    | 1   | True  |
| 1    | 2   | False |
| 1    | 3   | True  |

```python
import numpy as np

def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))

nft1 = np.array([0.5, 0.5, 0.5, 0.5])
nft2 = np.array([0.5, 0.5, 0.5, 0.5])

euclidean_distance(nft1, nft2)
```

## User profiles
By using the blockchain, we can obtain some demographics about the customer.  These properties may include:

* First seen on chain
* Trade history and transaction volume
* Trade frequency
* Balances
* Holding time
* Previous NFT sale history

For this POC we will only use current balance as a dimension.

## The tech stack

<img width="1101" alt="image" src="https://github.com/bitcoinbrisbane/coordinates-tinder/assets/8411406/8fc8aad7-4500-470e-a3c3-a62e0a1357d7">

- Python FastAPI for the API
- React for the front end
- Tensorflow for the machine learning
- MongoDB for the database
- Redis if required for caching

## Work flow

### New users

- Look up wallet
- Cache data
- Offer suggestions

## Start the API

```bash
docker-compose up
uvicorn main:app --reload
```

### API

Suggest next ordinal

- GET /?address=bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297

```json
{
  "id": "6abcb215dae6058653f4ba4d717a00fca46ac8c3dea46876057c128f3786f892i0",
  "number": 1162315496355503,
  "address": "bc1paxxeugh54jvrqcwz0hwjlnt4tktuef5jfmfp6tn77x5cdjkrtf3q2lqgh4",
  "value": 1000,
  "image": "https://api.example.com/image/1162315496355503",
  "metadata": {
  }
}
```

Post feedback

- POST /index
```json
{
  "liked": true
}
```

### Training

To obtain more dimensions, we need to abstract meta data or properties from the NFT.  This could be done by hand, or by using a machine learning model to extract the properties.


```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

```bash
python train.py
```

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Assume you have your training data in `train_images` and `train_labels`
# train_images = ...
# train_labels = ...

# Train the model
model.fit(train_images, train_labels, epochs=10, batch_size=32)

# Assume you have your test data in `test_images` and `test_labels`
# test_images = ...
# test_labels = ...

# Evaluate the model
model.evaluate(test_images, test_labels)
```

### Front end

```javascript
import React from 'react';
import { useSwipeable } from 'react-swipeable';
import axios from 'axios';

function SwipeableImage({ imageUrl, onSwipe }) {
  const handlers = useSwipeable({
    onSwipedLeft: () => handleSwipe('left'),
    onSwipedRight: () => handleSwipe('right'),
    preventDefaultTouchmoveEvent: true,
    trackMouse: true
  });

  const handleSwipe = (direction) => {
    console.log(`Swiped ${direction}`);
    onSwipe(direction);

    // Post to API
    axios.post('YOUR_API_ENDPOINT', {
      image: imageUrl,
      swipeDirection: direction
    })
    .then(response => {
      console.log('Response from API:', response.data);
    })
    .catch(error => {
      console.error('Error posting to API:', error);
    });
  };

  return (
    <div {...handlers} style={{ width: '300px', height: '300px', overflow: 'hidden' }}>
      <img src={imageUrl} alt="Swipeable" style={{ width: '100%', height: '100%' }} />
    </div>
  );
}

export default SwipeableImage;

```

### Installation
```bash
yarn install coordinates-tinder
```

## Running the Python API
```bash
uvicorn main:app --reload
```

## References

- https://realpython.com/build-recommendation-engine-collaborative-filtering/
- https://www.tensorflow.org/recommenders
- https://www.youtube.com/watch?v=v90un9ALRzw&list=PLQY2H8rRoyvy2MiyUBz5RWZr5MPFkV3qz&index=2