# programmers 과제 테스트 템플릿 - Django

programmers의 과제 테스트는 코드를 제출하면 자동으로 서버를 구성하여 실행해 볼 수 있는 환경을 제공합니다. 

아래 내용을 확인하여 프로젝트를 구성하고 코드를 제출해 주세요.

> 참고: 데이터베이스 환경을 위해 `settings.py` 가 `settings/local.py` 와 `settings/production.py` 로 분리되어 있으며, 기본 settings로 `settings.production` 이 설정되어 있습니다.
>
> 따라서 로컬에서 실행이나 마이그레이션 등을 위해서는 다음과 같이 `--settings=myapp.settings.local` 옵션을 붙여주어야 합니다.
>
> ```shell
> $ python manage.py runserver --settings=myapp.settings.production
> $ python manage.py migrate --settings=myapp.settings.local
> ```



## Procfile

programmers의 과제 테스트는 내부적으로 [heroku buildpack](https://devcenter.heroku.com/)을 통해 제출한 코드를 실행합니다. 따라서 `Procfile` 이라는 **특별한 파일**이 프로젝트에 포함되어 있어야 합니다. 이 Procfile에는 앱 프로세스를 실행하는 명령이 지정되어 있어야 합니다.

Procfile은 프로세스 유형을 개별 라인에 선언합니다. 각 라인은 다음 형식으로 되어 있어야 합니다.

```
<프로세스 유형>: <명령>
```

`Procfile` 을 사용하여 다음과 같은 프로세스 유형을 선언 할 수 있습니다.

- **web**: 웹 서버 프로세스를 실행하는 명령을 지정할 수 있습니다. 예를 들면 django에서는 다음과 같이 정의 할 수 있습니다.

  ```
  web: gunicorn mysite.wsgi --log-file -
  ```

- **migrate**: programmers의 과제 테스트는 코드를 실행 시, 매번 새로운 데이터베이스 서버를 실행합니다. 따라서 데이터베이스에 테이블을 생성하는 명령을 이 유형에 정의 해야합니다.

  ```
  migrate: python manage.py migrate --settings=myapp.settings.production
  ```

  >  **주의!**: migrate 유형은 반드시 정의되어 있어야 합니다. 만약 서버 실행시 자동으로 db가 sync되어 이 명령이 필요없다면 다음과 같이 정의해주세요.

    ```
    migrate: /bin/true
    ```

- **seed**: 초기 데이터를 데이터베이스에 입력하기 위한 명령을 지정합니다. migrate 이후에 실행됩니다.

  ```
  seed: python manage.py loaddata myapp/item/fixtures/items-data.json
  ```

- 이외에 다른 프로세스 유형은 지원하지 않습니다.



## 데이터베이스

programmers의 과제 테스트에서는 현재 **MySQL**만 지원하며, 다른 데이터베이스 엔진은 지원하지 않습니다.

데이터베이스와 관련되어 정의되어 있는 환경 변수들은 다음과 같습니다.

  - MySQL 접속 host: `MYSQL_ROOT_HOST=mysql-server`

  - MySQL 유저: `MYSQL_USER=root`

  - MySQL 유저의 비밀번호: `MYSQL_ROOT_PASSWORD=password`

  - 사전에 생성된 데이터베이스: `MYSQL_DATABASE=my_database`

  > 참고: 이 템플릿의 `myapp/settings/production.py` 에 정의되어 있는 값들을 참고해주세요.

programmers에서 과제를 자동으로 실행할 때에는 마이그레이션을 위해 서버 실행 전 Procfile 파일의 **migrate**에 정의되어 있는 명령을 실행합니다.

본 템플릿에는 데이터베이스 마이그레이션의 예시로 `item` model이 정의되어 있습니다. 이를 참고하여 필요한 model의 마이그레이션을 구성해주세요.

  ```python
  class Item(models.Model):
      name = models.CharField(max_length=32)
      quantity = models.IntegerField()
  ```
  
마이그레이션과 마찬가지로 초기 데이터를 데이터베이스에 입력하기 위해 Procfile 파일의 **seed** 에 정의된 명령을 수행합니다.

> 참고: 마찬가지로 `‌myapp/item/fixtures/items-data.json` 디렉토리에 db seeding 예시가 정의되어 있습니다.
  
실행 시, 매번 새로운 데이터베이스 서버가 실행되며, 실행이 종료되면 데이터베이스 내의 데이터는 삭제됩니다.



## 실행 및 제출 시 주의사항

- Port 번호는 **PORT 환경 변수** 또는 **5000** 을 사용해야 합니다.

- Procfile에는 Django 애플리케이션에 권장하는 프로덕션 웹 서버인 **Gunicorn** 패키지와 static 파일 관리를 위한 **WhiteNoise** 패키지를 설치해야 합니다. `virtualenv` 활성화 상태에서 다음 명령어로 설치 할 수 있습니다.

  ```shell
  (env) $ pip install dj-database-url gunicorn whitenoise
  ```

- programmers에서 과제 실행 및 제출 시에는 build 중 `$ python manage.py collectstatic --noinput` 명령을 자동으로 실행합니다. collectstatic 단계가 실패하면 빌드가 실패합니다. 

- 저장소의 루트 디렉토리에는 `Pipfile` 함께 `requirements.txt` 파일이 포함되어 있어야합니다.

	`requirements.txt` 은 종속성 패키지가 정의되어 있어야하며 다음 명령으로 파일을 생성할 수 있습니다. 자세한 내용은 [여기](https://pip.pypa.io/en/stable/user_guide/#requirements-files)을 확인해주세요.

    ```shell
  (env) $ pip freeze > requirements.txt
    ```

- stdout으로 출력된 로그는 화면에 표시됩니다.

- programmers에서 실행된 서버는 최대 10분 뒤에는 자동으로 종료됩니다.



## 실행 및 제출 방법

1.  **본인의 github 계정**의 **private** 저장소를 생성해서 과제를 **master** 브랜치에 push 해주세요.

     > **주의!**: 저장소가 public으로 되어 있는 경우에는 programmers에서 과제를 실행/제출할 수 없습니다.

2. github 저장소 페이지의 **Setting > Collaborators** 에서 [programmers-gitbot](https://github.com/programmers-gitbot) 을 Collaborator로 추가 해주세요.

3. 실행시 github 저장소의 url을 입력하시고 **[빌드(build)]** 버튼을 누르면 자동으로 서버를 구성하여 실행 합니다. 실행 후에는 **[최종 제출]** 버튼이 활성화되어 과제를 제출 할 수 있습니다.

4. **[최종 제출] 하면 테스트가 종료되며, 이후 다시 제출이 불가능하니 충분히 실행을 해보시고 제출하시기 바랍니다!!**

   > **주의!**: [최종 제출] 되면 제출 당시의 master 브랜치의 commit으로 제출이 고정되므로 제출 이후 저장소에 commit을 push 해도 제출물에는 반영되지 않습니다.


## 에러 로그 발생 시 참고사항

- git fetch failed! please check your repository.

  > 잘못된 저장소 주소를 입력하거나 force commit으로 해당 commit이 없어진 경우 발생합니다.

- -----> Unable to select a buildpack

  > 저장소 root 디렉토리에 `requirements.txt` 파일이나 `manage.py` 파일을 찾을 수 없습니다. 저장소에 해당 파일을 확인해주세요.

- No matching distribution found for '...'

  > `requirements.txt` 에 정의 된 패키지를 찾을 수 없습니다. `requirements.txt` 파일을 확인해주세요.

- Error while running '$ python manage.py collectstatic --noinput'.

  > collectstatic 명령이 실패했습니다. `static` 디렉토리와 settings의 `STATIC_*` 설정들을 확인해주세요. 

- ERROR: connect ECONNREFUSED 127.0.0.1:3306

  > MySQL host를 찾을 수 없습니다. MySQL host는 *MYSQL_ROOT_HOST* 환경변수 혹은 "mysql-server" 이여야 합니다.

  > **주의!**: programmers에서 과제 실행 시 MySQL host는 127.0.0.1(localhost)가 아니라 *mysql-server*임을 유의해주세요.

- ERROR: Access denied for user 'root'@'172.17.0.3' (using password: YES)

  > MySQL 유저 혹은 비밀번호를 잘못 입력했습니다. 유저는 *MYSQL_USER* 환경 변수 혹은 "root", 비밀번호는 *MYSQL_ROOT_PASSWORD* 환경 변수 혹은 "password" 이여야 합니다.

  > **주의!**: 이 로그에서 나오는 ip 주소를 고정으로 사용하지 마세요. MySQL host의 ip 주소는 동적으로 변할 수 있습니다.

- ERROR: Unknown database

  > database를 찾을 수 없습니다. database는 *MYSQL_DATABASE* 환경 변수 혹은 "my_database" 이여야 합니다.

- Proc entrypoint migrate does not exist. Please check your Procfile

  > 저장소 root 디렉토리에 Procfile 파일을 찾을 수 없거나 Procfile의 migrate가 정의되어 있지 않은 경우 발생합니다. 

- 페이지가 작동하지 않습니다.

  > 서버 실행에 실패했거나 서버가 실행된지 10분이 지나 종료되었습니다. Procfile의 web을 확인하여 서버 실행의 이상이 없는지 확인하세요. 이상이 없으면 [초기화] 후 다시 실행하세요.



## 원격 서버 시스템 및 프레임워크

실행하거나 제출된 application은 원격 서버에서 다음과 같은 시스템 및 프레임워크 환경에서 실행됩니다.
```
OS 버전: ubuntu 16.04
메모리 제한: 512 MiB
MySQL 버전: 8.0.17
python 버전: 3.6.7
```