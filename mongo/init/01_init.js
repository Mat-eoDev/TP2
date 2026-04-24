db = db.getSiblingDB(process.env.MONGO_DB || "blog_db");

db.createCollection("posts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "content", "author", "created_at"],
      properties: {
        title: { bsonType: "string" },
        content: { bsonType: "string" },
        author: { bsonType: "string" },
        created_at: { bsonType: "date" }
      }
    }
  }
});

db.posts.insertMany([
  { title: "Post 1", content: "Content 1", author: "Alice", created_at: new Date() },
  { title: "Post 2", content: "Content 2", author: "Bob", created_at: new Date() },
  { title: "Post 3", content: "Content 3", author: "Charlie", created_at: new Date() },
  { title: "Post 4", content: "Content 4", author: "Diana", created_at: new Date() },
  { title: "Post 5", content: "Content 5", author: "Eve", created_at: new Date() }
]);
