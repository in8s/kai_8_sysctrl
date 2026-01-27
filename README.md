# kai_8_sysctrl

🚧 PROJECT STILL IN PROGRESS 🚧

Hi!  
Thanks for checking out this project.  
Feel free to leave any feedback or suggestions — I’m always looking for ways to improve both code quality and efficiency.

---

## 📅 27.01.2026

This project is a dashboard for managing your PC remotely.

At the current early stage of development, the application works locally only — there is no port forwarding or public internet access yet.  
Remote access over the internet is planned after a proper security update and basic penetration testing.

### Current features
- Restarting the system
- Logging out
- Shutting down
- Making backups
- Fetching basic system information

### Planned features
- Network scanning using **nmap** via command-line integration
- Improved authentication and security
- Remote access over the internet
- Frontend upgrade

---

## 🛠 Technologies

### Backend
- **FastAPI**  
  https://fastapi.tiangolo.com/
- Basic HTTP authentication  
  *(major security update planned)*

To run the backend locally:
```bash
uvicorn main:app --reload
