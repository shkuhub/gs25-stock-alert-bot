# Android / 우리동네GS 자동화 테스트

현재 GS25 원본 재고 endpoint는 이 환경에서 HTTP 403을 반환하고, 공개 relay는 운영자의 GS25_API_KEY가 없어 503을 반환합니다.

따라서 MVP 검증은 사용자가 직접 설치한 공식 우리동네GS Android 앱(com.gsr.gs25)을 ADB로 조작하는 경로로 진행합니다.

## 준비

Android 공식 Platform-Tools를 설치하고 adb를 PATH에 추가합니다.

실제 Android 기기를 쓰는 경우:
1. 개발자 옵션 활성화
2. USB 디버깅 활성화
3. USB 연결
4. 기기에서 USB 디버깅 허용

확인:
    adb devices

정상적으로 device가 표시되면 연결 완료입니다.

Android 공식 문서:
https://developer.android.com/tools/adb
https://developer.android.com/studio/run/device

## GS25 앱 실행 및 UI 확인

가상환경이 켜진 상태에서 프로젝트 루트에서:

    .\scripts\android\open_gs25_inventory.ps1

기본 좌표는 공개된 GS25 ADB 재현 예시입니다. 휴대폰 해상도에 따라 맞지 않을 수 있습니다.

실행 후 현재 화면의 UI hierarchy가:
    data\android\window.xml

에 저장됩니다.

## 다음 단계

UI hierarchy에서 상품명, 매장명, 재고 수량이 실제로 노출되는지 확인합니다.

확인되면:
1. 상품 4개를 재고찾기에서 선택하는 자동화
2. 목록보기 전환
3. 매장명/재고 수량 파싱
4. SQLite 상태 저장
5. 0 → 1 이상 재입고 감지
6. 5분 polling
7. 안정성 확인 후 polling 주기 조정
8. Threads 게시 연결

앱의 인증정보나 비밀 키를 추출하는 방식은 사용하지 않습니다.
