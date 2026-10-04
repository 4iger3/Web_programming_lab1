#!/bin/bash
cd /home/iger/Документы/node-lab-website
mkdir -p screenshots
# Screenshot 1: Task 1 - Node and NPM versions in terminal
gnome-terminal -- bash -c 'echo "=== Node.js ==="; node -v; echo "=== npm ==="; npm -v; echo "=== DONE ==="; exec bash' &
sleep 2
gnome-screenshot -f screenshots/task1_node_versions.png --include-pointer
# Screenshot 2: Task 4 - website running
DISPLAY=:0 firefox --headless -screenshot screenshots/task4_website_running.png http://localhost:3000
# Screenshot 3: Task 2 - project tree in file manager
gnome-terminal -- bash -c 'tree -L 2 -I node_modules; echo ""; echo "Press Enter to exit..."; read' &
sleep 2
gnome-screenshot -f screenshots/task2_project_tree.png --include-pointer
# Screenshot 4: Task 5/6 - website with CSS and JS
DISPLAY=:0 firefox --headless -screenshot screenshots/task5_website_css.png http://localhost:3000
echo "Screenshots taken"
ls -la screenshots/
