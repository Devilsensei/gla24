import React from "react";
import "./post.css";

const Post = () => {
  return (
    <div className="post">
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
          src="https://via.placeholder.com/600x400"
          alt="Post content"
          className="post-content"
        />
      </div>

      {/* Post Actions */}
      <div className="post-actions">
        <div className="left-actions">
          <img
            src="https://img.icons8.com/ios-glyphs/30/000000/like--v1.png"
            alt="Like"
          />
          <img
            src="https://img.icons8.com/ios-glyphs/30/000000/topic.png"
            alt="Comment"
          />
          <img
            src="https://img.icons8.com/ios-filled/30/000000/share.png"
            alt="Share"
          />
        </div>
        <div className="right-action">
          <img
            src="https://img.icons8.com/ios-filled/30/000000/bookmark-ribbon.png"
            alt="Save"
          />
        </div>
      </div>

      {/* Like and Comment Counter */}
      <div className="post-likes">
        <span>Liked by <strong>user1</strong> and <strong>others</strong></span>
      </div>

      <div className="post-caption">
        <strong>username</strong> This is the caption for the post...
      </div>

      <div className="post-comments">
        <strong>View all 12 comments</strong>
        <div className="comment">
          <strong>user2</strong> This is a comment.
        </div>
      </div>

      {/* Add Comment */}
      <div className="post-add-comment">
        <input
          type="text"
          className="add-comment-input"
          placeholder="Add a comment..."
        />
        <button className="post-comment-btn">Post</button>
      </div>
    </div>
  );
};

export default Post;
