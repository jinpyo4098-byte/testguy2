Gravity Arrow 게임 정적 배포
=======================

이 리포지토리는 `index.html`과 `game.js`로 구성된 정적 HTML 게임입니다.

사용 방법
---------

1. 브라우저에서 `index.html` 파일을 열면 게임이 표시됩니다.
2. Cloudflare Pages에 배포하려면 다음을 설정하세요:
   - 빌드 명령: 비워둡니다.
   - 게시 디렉터리: `/` 또는 리포지토리 루트
   - `index.html`이 루트에 있어야 합니다.

Cloudflare Pages 자동 배포
------------------------

- 이 저장소가 Cloudflare Pages에 연결된 경우, `main` 브랜치로 푸시하면 변경 내용이 자동으로 배포됩니다.
- 이미 연결되어 있지 않다면 Cloudflare Pages에서 GitHub 저장소를 추가하고 루트 디렉터리를 배포 대상으로 지정하세요.

참고
----

- `app.py`는 Streamlit용 인라인 HTML 버전이며, Cloudflare Pages 정적 사이트 배포에는 사용되지 않습니다.
- `index.html`과 `game.js`가 현재 실제 실행 가능한 게임 프론트엔드입니다.
