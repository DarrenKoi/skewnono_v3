<template>
  <div class="min-h-screen bg-surface-0 dark:bg-surface-950 py-8">
    <div class="container mx-auto px-4 max-w-4xl">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="flex items-center justify-center gap-4 mb-6">

          <h1 class="text-4xl font-bold text-surface-900 dark:text-surface-0">SKEWNONO</h1>
        </div>
        <p class="text-lg text-surface-700 dark:text-surface-300 max-w-2xl mx-auto">
          첨단 반도체 제조 모니터링 및 분석 플랫폼
        </p>
      </div>

      <!-- About Section -->
      <Card class="mb-8">
        <template #title>
          <div class="flex items-center gap-2">
            <i class="pi pi-info-circle text-primary-500" />
            <span>SKEWNONO 소개</span>
          </div>
        </template>
        <template #content>
          <div class="space-y-4">
            <p class="text-surface-700 dark:text-surface-300">
              SKEWNONO는 반도체 제조 현장의 장비 성능, 공정 통계, 운영 효율성을 실시간으로 파악할 수 있도록 설계된 통합 모니터링 시스템입니다. 프라이빗 클라우드 환경에 최적화되어, 최소한의
              리소스로 강력한 모니터링 기능을 제공합니다.
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex items-start gap-3">
                <i class="pi pi-chart-line text-primary-500 mt-1" />
                <div>
                  <h4 class="font-semibold text-surface-900 dark:text-surface-0">실시간 모니터링</h4>
                  <p class="text-sm text-surface-600 dark:text-surface-400">장비 상태 및 성능 지표를 실시간으로 확인</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <i class="pi pi-database text-primary-500 mt-1" />
                <div>
                  <h4 class="font-semibold text-surface-900 dark:text-surface-0">데이터 분석</h4>
                  <p class="text-sm text-surface-600 dark:text-surface-400">공정 최적화를 위한 고급 분석 기능</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <i class="pi pi-cog text-primary-500 mt-1" />
                <div>
                  <h4 class="font-semibold text-surface-900 dark:text-surface-0">장비 관리</h4>
                  <p class="text-sm text-surface-600 dark:text-surface-400">하드웨어 모니터링 및 제어 기능 제공</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <i class="pi pi-search text-primary-500 mt-1" />
                <div>
                  <h4 class="font-semibold text-surface-900 dark:text-surface-0">레시피 검색</h4>
                  <p class="text-sm text-surface-600 dark:text-surface-400">지능형 레시피 및 공정 파라미터 검색</p>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Tech Stack Section -->
      <Card class="mb-8">
        <template #title>
          <div class="flex items-center gap-2">
            <i class="pi pi-code text-primary-500" />
            <span>기술 스택</span>
          </div>
        </template>
        <template #content>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Backend -->
            <div>
              <h4 class="font-semibold text-surface-900 dark:text-surface-0 mb-4 flex items-center gap-2">
                <i class="pi pi-server text-blue-500" />
                백엔드 기술
              </h4>
              <div class="space-y-3">
                <div class="flex items-center gap-3">
                  <Badge value="Flask" severity="success" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">Python 웹 프레임워크</span>
                </div>
                <div class="flex items-center gap-3">
                  <Badge value="Redis" severity="danger" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">인메모리 데이터 저장소 및 캐싱</span>
                </div>
                <div class="flex items-center gap-3">
                  <Badge value="uWSGI" severity="info" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">애플리케이션 서버</span>
                </div>
                <div class="flex items-center gap-3">
                  <Badge value="Elasticsearch" severity="warning" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">검색 및 분석 엔진</span>
                </div>
              </div>
            </div>

            <!-- Frontend -->
            <div>
              <h4 class="font-semibold text-surface-900 dark:text-surface-0 mb-4 flex items-center gap-2">
                <i class="pi pi-desktop text-green-500" />
                프론트엔드 기술
              </h4>
              <div class="space-y-3">
                <div class="flex items-center gap-3">
                  <Badge value="Vue 3" severity="success" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">진보적인 자바스크립트 프레임워크</span>
                </div>
                <div class="flex items-center gap-3">
                  <Badge value="PrimeVue" severity="primary" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">UI 컴포넌트 라이브러리</span>
                </div>
                <div class="flex items-center gap-3">
                  <Badge value="Tailwind CSS" severity="info" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">유틸리티 기반 CSS 프레임워크</span>
                </div>
                <div class="flex items-center gap-3">
                  <Badge value="Vite" severity="warning" />
                  <span class="text-sm text-surface-600 dark:text-surface-400">빌드 도구 및 개발 서버</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- FAQ Section -->
      <Card>
        <template #title>
          <div class="flex items-center gap-2">
            <i class="pi pi-question-circle text-primary-500" />
            <span>자주 묻는 질문</span>
          </div>
        </template>
        <template #content>
          <Accordion multiple>
            <AccordionPanel value="0">
              <AccordionHeader>SKEWNONO는 어떤 용도로 사용되나요?</AccordionHeader>
              <AccordionContent>
                <p class="text-surface-700 dark:text-surface-300">
                  SKEWNONO는 반도체 제조 환경에서 장비 성능 모니터링, 공정 통계 추적, 하드웨어 자원 관리, 운영 최적화를 위한 분석 인사이트 제공을 위해 설계되었습니다.
                </p>
              </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="1">
              <AccordionHeader>시스템 요구사항은 어떻게 되나요?</AccordionHeader>
              <AccordionContent>
                <p class="text-surface-700 dark:text-surface-300">
                  본 애플리케이션은 2코어 CPU와 8GB RAM을 갖춘 프라이빗 클라우드 환경에 최적화되어 있습니다. 캐싱을 위해 Redis가 필요하며, 검색 기능을 위해 Elasticsearch
                  v7이 필요합니다.
                </p>
              </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="2">
              <AccordionHeader>어떻게 배포하나요?</AccordionHeader>
              <AccordionContent>
                <p class="text-surface-700 dark:text-surface-300">
                  백엔드는 Flask와 uWSGI로 프로덕션 환경에서 구동되며, 프론트엔드는 정적 SPA로 빌드됩니다. 내부망에서만 접근 가능한 프라이빗 클라우드 환경에 배포하도록 설계되었습니다.
                </p>
              </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="3">
              <AccordionHeader>어떤 모니터링 기능을 제공하나요?</AccordionHeader>
              <AccordionContent>
                <p class="text-surface-700 dark:text-surface-300">
                  SKEWNONO는 실시간 장비 상태 모니터링, 디바이스 통계 추적, 장애 이슈 분석, 하드웨어 관리, 레시피 검색 등 반도체 제조 현장에 필요한 다양한 모니터링 기능을 제공합니다.
                </p>
              </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="4">
              <AccordionHeader>API 문서가 제공되나요?</AccordionHeader>
              <AccordionContent>
                <p class="text-surface-700 dark:text-surface-300">
                  본 애플리케이션은 헬스 체크, 작업 상태 모니터링, 사용자 관리를 위한 RESTful API 엔드포인트를 제공합니다. API 문서는 개발 환경에서 확인하거나 코드베이스의 라우트를
                  참고하실 수 있습니다.
                </p>
              </AccordionContent>
            </AccordionPanel>
          </Accordion>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import Card from 'primevue/card'
import Badge from 'primevue/badge'
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
</script>
