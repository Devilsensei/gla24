import React, { useState } from 'react';
import './notification.css';

const NotificationPage = () => {
  const [liked, setLiked] = useState(false);

  const handleNotification = () => {
    if ('Notification' in window) {
      if (Notification.permission === 'granted') {
        new Notification('You liked the post!');
      } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            new Notification('You liked the post!');
          }
        });
      }
    } else {
      alert('This browser does not support notifications.');
    }
  };

  const handleLikeClick = () => {
    setLiked(!liked);
    handleNotification();
  };

  return (
    <div className="post-container">
      {/* Post Header */}
      <div className="post-header">
        <img
          src="https://via.placeholder.com/50"
          alt="Profile"
          className="profile-pic"
        />
        <div className="post-user-info">
          <span className="username">username</span>
          <span className="location">Location</span>
        </div>
        <div className="post-options">...</div>
      </div>

      {/* Post Image */}
      <div className="post-image">
        <img
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ76EZo9M5zFqizIccxd7PI8BA8ujlQEbpzgg&s"
          alt="Post content"
          className="post-content"
        />
      </div>

      {/* Like Button */}
      <div className="like-section">
        <button className={`like-button ${liked ? 'liked' : ''}`} onClick={handleLikeClick}>
          <span className="heart-icon">{liked ? '❤️' : '🤍'}</span>
        </button>
      </div>
    </div>
  );
};

export default NotificationPage;
