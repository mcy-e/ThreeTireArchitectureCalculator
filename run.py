from App import create_app
import os
import logging

app = create_app()

if __name__ == '__main__':
    #* logging (recommended by AI)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        #* run the app 
        logging.info("Flask server started successfully")
        app.run(
            debug=True,
            host=os.environ.get('FLASK_HOST', '127.0.0.1'),  
            port=int(os.environ.get('FLASK_PORT', 5000)),    
        )
        
    
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}", exc_info=True)
        raise  