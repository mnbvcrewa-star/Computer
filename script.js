function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            
            // สลับคลาส active เพื่อแสดง/ซ่อน Sidebar
            sidebar.classList.toggle('active');
            
            // แสดง/ซ่อนฉากหลังมืด
            if (sidebar.classList.contains('active')) {
                overlay.style.display = 'block';
            } else {
                overlay.style.display = 'none';
            }
        }