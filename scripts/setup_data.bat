@echo off
echo Setting up Medocker data directory from templates...

if not exist "data" mkdir data

:: Copy template directories only if they don't exist
if not exist "data\keycloak" xcopy "data-templates\keycloak" "data\keycloak" /E /I /Y
if not exist "data\mariadb" xcopy "data-templates\mariadb" "data\mariadb" /E /I /Y
if not exist "data\mattermost" xcopy "data-templates\mattermost" "data\mattermost" /E /I /Y
if not exist "data\nextcloud" xcopy "data-templates\nextcloud" "data\nextcloud" /E /I /Y
if not exist "data\openemr" xcopy "data-templates\openemr" "data\openemr" /E /I /Y
if not exist "data\portainer" xcopy "data-templates\portainer" "data\portainer" /E /I /Y
if not exist "data\postgres" xcopy "data-templates\postgres" "data\postgres" /E /I /Y
if not exist "data\rustdesk" xcopy "data-templates\rustdesk" "data\rustdesk" /E /I /Y
if not exist "data\traefik" xcopy "data-templates\traefik" "data\traefik" /E /I /Y
if not exist "data\vaultwarden" xcopy "data-templates\vaultwarden" "data\vaultwarden" /E /I /Y

echo Data directory setup complete! 