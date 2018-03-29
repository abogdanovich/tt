
db.temp_users.insert(
   {
      _id: "userid",
      seq: NumberInt(0)
   }
)

function getNextSequence(value) {
   var ret = db.temp_users.findAndModify(
          {
            query: { _id: value },
            update: { $inc: { seq: NumberInt(1) } },
            new: true
          }
   );
   return ret.seq;
}


db.temp_users.insert(
   {
     user_id: getNextSequence("userid"),
     name: "Sarah Conor"
   }
);


db.temp_users.update({"_id": {$ne: "userid"} }, { $set: {user_id: getNextSequence("userid")}}, false, true);

db.temp_users.update({"_id": {$ne: "userid"} }, { $set: {user_id: getNextSequence("userid")}});

db.temp_users.update({"_id": {$ne: "userid"} }, { $set: {user_id: getNextSequence("userid")}}, {upsert: false, multi: true});


db.temp_users.update({"_id": {$ne: "userid"}, got_userid: { $exists: false } }, { $set: {user_id: getNextSequence("userid"), got_userid: true}}, {upsert: false, multi: true});
db.temp_users.update({"_id": {$ne: "userid"}, got_userid: { $exists: true } }, { $unset: { got_userid: true}}, {upsert: false, multi: true});
db.temp_users.update({"_id": {$ne: "userid"}, userid: { $exists: true } }, { $unset: { _userid: true}}, {upsert: false, multi: true});



db.users.find({"_id": ObjectId("54365ea64f452d326a084f26")})
db.users.update({"_id": ObjectId("54365ea64f452d326a084f26")}, {$unset: {"userid": true}})
db.users.update({"userid": {$exists: true}}, {$unset: {"userid": true}}, {multi: true})







