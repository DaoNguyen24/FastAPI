from fastapi import APIRouter,Response,status,HTTPException,Depends
from .. import schemas,oauth2,main


router = APIRouter(prefix="/votes", tags=["vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote,user_id:int =Depends(oauth2.get_curent_user)):
    #Tim xem vote da ton tai chua
    main.cursor.execute("SELECT * FROM votes WHERE user_id = %s AND post_id = %s",(str(user_id.id),vote.post_id,))
    found_vote = main.cursor.fetchall()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {user_id.id} has already vote on post {vote.post_id}")
        else:
            main.cursor.execute("INSERT INTO votes (user_id, post_id) VALUES (%s,%s) RETURNING * ",(user_id.id,vote.post_id,))
            vote_changes = main.cursor.fetchone()
            main.connect.commit()
            return {"vote_added" : vote_changes }
    else:
        if found_vote:
            main.cursor.execute('''DELETE FROM votes WHERE user_id = %s AND post_id = %s RETURNING *''', (user_id.id,vote.post_id,))
            vote_changes = main.cursor.fetchone()
            main.connect.commit()
            return {"vote_deleted": vote_changes}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post{vote.post_id} hasnt been voted by user {user_id.id}")
        
    
         