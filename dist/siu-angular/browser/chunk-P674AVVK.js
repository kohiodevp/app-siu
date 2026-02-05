import{a as oe,b as Dt,c as It}from"./chunk-6DOQAXWL.js";import{a as bt,b as vt,c as St,d as Pt,e as wt,f as Mt,g as yt,h as Et,i as Ot,j as Tt,l as kt}from"./chunk-3DRFPNYN.js";import{a as ne,b as Lt}from"./chunk-TUX7OWEK.js";import{b as jt}from"./chunk-MXF6346I.js";import{a as Rt,b as Nt,c as zt}from"./chunk-2UDASV47.js";import"./chunk-7UZYWCAJ.js";import{a as qt,b as Ce,c as Ht}from"./chunk-DN6ZU6PW.js";import{c as Vt,g as At}from"./chunk-MR57I2Q4.js";import{a as $t,b as Ft}from"./chunk-D4D64KG6.js";import{a as Bt}from"./chunk-VUQ35JGS.js";import{c as _e,d as fe,g as V,i as ge,j as De,k as Ie}from"./chunk-OCAOS45R.js";import{b as _t}from"./chunk-5MZAGVAN.js";import{a as lt,b as ct}from"./chunk-HD4V77CK.js";import{a as xt}from"./chunk-U4ARKFAA.js";import{d as gt,h as Ct,i as ht}from"./chunk-M2B5FNU7.js";import{b as ee,d as te,f as ie}from"./chunk-TC4NHXKF.js";import"./chunk-CVA3OUYK.js";import{b as it,c as nt}from"./chunk-E7OICD5F.js";import{a as tt}from"./chunk-OFBHONAA.js";import{b as Ke,e as Xe,i as et}from"./chunk-YPBVTN56.js";import{b as ot}from"./chunk-3WYC6ROS.js";import{a as dt,b as mt,c as pt,d as ut}from"./chunk-QECNG6W7.js";import"./chunk-AC4QEAXS.js";import{c as st}from"./chunk-QLHDTFGW.js";import{a as X}from"./chunk-TAVIRTLO.js";import{a as K}from"./chunk-RSTPHI64.js";import{a as ft}from"./chunk-4PMYLZD4.js";import{a as rt}from"./chunk-XMY2MG46.js";import{p as at}from"./chunk-QDNYLZKO.js";import{a as U,b as Je,c as Ze,d as Qe,e as Ye,f as We,h as G}from"./chunk-FY6NZ6SC.js";import{b as Ve,g as Ae,h as Re,k as Ne,l as ze,m as je,n as Be,p as qe,s as He,t as Ue,u as Ge}from"./chunk-4TEKNYBZ.js";import{a as Y,b as W}from"./chunk-UUJ2B6HP.js";import{a as Fe}from"./chunk-XNCRNYUB.js";import{$ as Q,W as J,Y as Z}from"./chunk-AQZ5PN4T.js";import{c as ke,d as H,g as Le}from"./chunk-JWWLDGKM.js";import{a as $e}from"./chunk-NYFRATJG.js";import{h as Te,k as j,n as B,p as q}from"./chunk-3AYM6UTQ.js";import{Ab as Me,B as ve,Cb as b,D as se,Db as v,Ec as z,Fb as ye,Gb as D,H as de,Hb as I,Ib as u,Jb as a,Kb as o,Lb as y,Pb as S,Qb as P,R as Se,Sb as C,U as Pe,Wb as _,Xa as c,Y as A,Yb as d,ac as Ee,ba as w,bc as me,cc as pe,e as xe,ga as m,gc as ue,ha as p,hc as E,ic as $,kc as r,l as be,lb as N,lc as h,mc as x,oa as R,rb as g,sa as M,tc as F,uc as Oe,va as we,wc as T,yc as k}from"./chunk-E7AQ6X4Y.js";import{a as O}from"./chunk-EQDQRRRY.js";var ae=class n{constructor(){this.api=w($e)}exportExcelFromAPI(e){return this.api.postBlob("/api/reports/export/excel",e||{})}exportCSVFromAPI(e){return this.api.postBlob("/api/reports/export/csv",e||{})}exportGeoJSONFromAPI(e){return this.api.postBlob("/api/reports/export/geojson",e||{})}exportPDFFromAPI(e){return this.api.postBlob("/api/reports/export/pdf",e||{})}exportShapefileFromAPI(e){return this.api.postBlob("/api/reports/export/shapefile",e||{})}exportKMLFromAPI(e){return this.api.postBlob("/api/reports/export/kml",e||{})}exportToCSV(e,t="parcelles.csv"){if(!e||e.length===0){console.warn("Aucune donn\xE9e \xE0 exporter");return}let i=["R\xE9f\xE9rence Cadastrale","Adresse","Superficie (m\xB2)","Zone","Statut","Cat\xE9gorie","Latitude","Longitude","Date de cr\xE9ation","Date de modification"],l=e.map(f=>[f.reference_cadastrale||f.reference||"",f.address||"",f.area?.toString()||"",f.zone||"",this.getStatusLabel(f.status),f.category||"",f.coordinates?.lat?.toString()||"",f.coordinates?.lng?.toString()||"",this.formatDate(f.created_at),this.formatDate(f.updated_at)]),s=[i.join(";"),...l.map(f=>f.map(ce=>`"${ce}"`).join(";"))].join(`
`);this.downloadFile(s,t,"text/csv;charset=utf-8;")}exportToExcel(e,t="parcelles.xls"){if(!e||e.length===0){console.warn("Aucune donn\xE9e \xE0 exporter");return}let i=`
      <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel">
      <head>
        <meta charset="UTF-8">
        <style>
          table { border-collapse: collapse; width: 100%; }
          th { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; border: 1px solid #ddd; }
          td { padding: 8px; border: 1px solid #ddd; }
          tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
      </head>
      <body>
        <table>
          <thead>
            <tr>
              <th>R\xE9f\xE9rence Cadastrale</th>
              <th>Adresse</th>
              <th>Superficie (m\xB2)</th>
              <th>Zone</th>
              <th>Statut</th>
              <th>Cat\xE9gorie</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Nombre de propri\xE9taires</th>
              <th>Nombre de documents</th>
              <th>Date de cr\xE9ation</th>
              <th>Date de modification</th>
            </tr>
          </thead>
          <tbody>
            ${e.map(l=>`
              <tr>
                <td>${l.reference_cadastrale||l.reference||""}</td>
                <td>${l.address||""}</td>
                <td>${l.area||""}</td>
                <td>${l.zone||""}</td>
                <td>${this.getStatusLabel(l.status)}</td>
                <td>${l.category||""}</td>
                <td>${l.coordinates?.lat||""}</td>
                <td>${l.coordinates?.lng||""}</td>
                <td>${l.owners?.length||0}</td>
                <td>${l.documents?.length||0}</td>
                <td>${this.formatDate(l.created_at)}</td>
                <td>${this.formatDate(l.updated_at)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </body>
      </html>
    `;this.downloadFile(i,t,"application/vnd.ms-excel")}exportToJSON(e,t="parcelles.json"){if(!e||e.length===0){console.warn("Aucune donn\xE9e \xE0 exporter");return}let i=JSON.stringify(e,null,2);this.downloadFile(i,t,"application/json")}exportToPDF(e,t="parcelles.pdf"){if(!e||e.length===0){console.warn("Aucune donn\xE9e \xE0 exporter");return}let i=window.open("","_blank");if(!i){console.error("Impossible d'ouvrir la fen\xEAtre d'impression");return}let l=`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Liste des Parcelles</title>
        <style>
          @media print {
            @page { size: A4 landscape; margin: 1cm; }
          }
          body { 
            font-family: Arial, sans-serif; 
            font-size: 10pt;
            margin: 0;
            padding: 20px;
          }
          h1 { 
            text-align: center; 
            color: #333;
            margin-bottom: 20px;
          }
          .metadata {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 9pt;
          }
          table { 
            width: 100%; 
            border-collapse: collapse;
            margin-top: 20px;
          }
          th { 
            background-color: #4CAF50; 
            color: white; 
            padding: 8px; 
            text-align: left;
            font-size: 9pt;
            border: 1px solid #ddd;
          }
          td { 
            padding: 6px 8px; 
            border: 1px solid #ddd;
            font-size: 9pt;
          }
          tr:nth-child(even) { background-color: #f9f9f9; }
          .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 8pt;
            color: #999;
          }
        </style>
      </head>
      <body>
        <h1>Syst\xE8me d'Information Urbain - Liste des Parcelles</h1>
        <div class="metadata">
          <p>Date d'export: ${new Date().toLocaleDateString("fr-FR",{year:"numeric",month:"long",day:"numeric",hour:"2-digit",minute:"2-digit"})}</p>
          <p>Nombre de parcelles: ${e.length}</p>
        </div>
        
        <table>
          <thead>
            <tr>
              <th>R\xE9f\xE9rence</th>
              <th>Adresse</th>
              <th>Superficie</th>
              <th>Zone</th>
              <th>Statut</th>
              <th>Propri\xE9taires</th>
              <th>Documents</th>
            </tr>
          </thead>
          <tbody>
            ${e.map(s=>`
              <tr>
                <td>${s.reference_cadastrale||s.reference||""}</td>
                <td>${s.address||"-"}</td>
                <td>${s.area?s.area+" m\xB2":"-"}</td>
                <td>${s.zone||"-"}</td>
                <td>${this.getStatusLabel(s.status)}</td>
                <td>${s.owners?.length||0}</td>
                <td>${s.documents?.length||0}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
        
        <div class="footer">
          <p>&copy; ${new Date().getFullYear()} SIU - Syst\xE8me d'Information Urbain</p>
        </div>
        
        <script>
          window.onload = function() {
            window.print();
            // Fermer apr\xE8s impression (optionnel)
            // window.onafterprint = function() { window.close(); }
          }
        <\/script>
      </body>
      </html>
    `;i.document.write(l),i.document.close()}downloadFile(e,t,i){let l=new Blob(["\uFEFF"+e],{type:i}),s=window.URL.createObjectURL(l),f=document.createElement("a");f.href=s,f.download=t,f.click(),window.URL.revokeObjectURL(s)}formatDate(e){return e?new Date(e).toLocaleDateString("fr-FR",{year:"numeric",month:"2-digit",day:"2-digit"}):""}getStatusLabel(e){return e?{available:"Disponible",occupied:"Occup\xE9e",disputed:"Contest\xE9e",reserved:"R\xE9serv\xE9e"}[e]||e:"Non d\xE9fini"}exportStatistics(e,t="statistiques.txt"){let i=this.calculateStatistics(e),l=`
STATISTIQUES DES PARCELLES
===========================
Date: ${new Date().toLocaleString("fr-FR")}

R\xC9SUM\xC9 G\xC9N\xC9RAL
--------------
Nombre total de parcelles: ${i.total}
Superficie totale: ${i.totalArea.toFixed(2)} m\xB2
Superficie moyenne: ${i.avgArea.toFixed(2)} m\xB2

R\xC9PARTITION PAR STATUT
-----------------------
${Object.entries(i.byStatus).map(([s,f])=>`${this.getStatusLabel(s)}: ${f}`).join(`
`)}

R\xC9PARTITION PAR ZONE
---------------------
${Object.entries(i.byZone).map(([s,f])=>`${s||"Non d\xE9finie"}: ${f}`).join(`
`)}

DOCUMENTS
---------
Total de documents: ${i.totalDocuments}
Moyenne par parcelle: ${i.avgDocuments.toFixed(1)}

PROPRI\xC9TAIRES
-------------
Total de propri\xE9taires: ${i.totalOwners}
Moyenne par parcelle: ${i.avgOwners.toFixed(1)}
    `.trim();this.downloadFile(l,t,"text/plain;charset=utf-8")}calculateStatistics(e){return{total:e.length,totalArea:e.reduce((t,i)=>t+(i.area||0),0),avgArea:e.reduce((t,i)=>t+(i.area||0),0)/e.length,byStatus:e.reduce((t,i)=>{let l=i.status||"undefined";return t[l]=(t[l]||0)+1,t},{}),byZone:e.reduce((t,i)=>{let l=i.zone||"undefined";return t[l]=(t[l]||0)+1,t},{}),totalDocuments:e.reduce((t,i)=>t+(i.documents?.length||0),0),avgDocuments:e.reduce((t,i)=>t+(i.documents?.length||0),0)/e.length,totalOwners:e.reduce((t,i)=>t+(i.owners?.length||0),0),avgOwners:e.reduce((t,i)=>t+(i.owners?.length||0),0)/e.length}}static{this.\u0275fac=function(t){return new(t||n)}}static{this.\u0275prov=A({token:n,factory:n.\u0275fac,providedIn:"root"})}};var re=class n{constructor(){this.datePipe=new j("fr-FR")}printParcel(e,t={}){let{includeOwners:i=!0,includeDocuments:l=!0,includeHistory:s=!0,includeQRCode:f=!0,logo:ce="/assets/logo.png"}=t,L=window.open("","_blank","width=800,height=600");if(!L){alert("Veuillez autoriser les popups pour imprimer");return}let Jt=this.generatePrintHTML(e,{includeOwners:i,includeDocuments:l,includeHistory:s,includeQRCode:f,logo:ce});L.document.write(Jt),L.document.close(),L.onload=()=>{setTimeout(()=>{L.print()},250)}}printMultipleParcels(e,t={}){let i=window.open("","_blank","width=800,height=600");if(!i){alert("Veuillez autoriser les popups pour imprimer");return}let l=this.generateMultiParcelsHTML(e,t);i.document.write(l),i.document.close(),i.onload=()=>{setTimeout(()=>{i.print()},250)}}generatePrintHTML(e,t){let i=this.datePipe.transform(new Date,"long"),l=t.includeQRCode?this.generateQRCodeDataURL(window.location.origin+"/parcels/"+e.id):"";return`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Parcelle ${e.reference} - Fiche d'Information</title>
        <style>
          ${this.getPrintStyles()}
        </style>
      </head>
      <body>
        <div class="print-container">
          <!-- Header -->
          <div class="print-header">
            <div class="header-left">
              ${t.logo?`<img src="${t.logo}" alt="Logo" class="logo">`:""}
              <div class="header-text">
                <h1>Syst\xE8me d'Information Urbaine</h1>
                <p>Fiche d'Information de Parcelle</p>
              </div>
            </div>
            <div class="header-right">
              ${l?`<img src="${l}" alt="QR Code" class="qr-code">`:""}
              <p class="print-date">Imprim\xE9 le ${i}</p>
            </div>
          </div>

          <!-- Title -->
          <div class="parcel-title">
            <h2>Parcelle ${e.reference}</h2>
            <span class="status-badge status-${e.status}">
              ${this.getStatusLabel(e.status)}
            </span>
          </div>

          <!-- Main Info -->
          <section class="section">
            <h3>Informations G\xE9n\xE9rales</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">R\xE9f\xE9rence cadastrale:</span>
                <span class="value">${e.reference}</span>
              </div>
              <div class="info-item">
                <span class="label">Adresse:</span>
                <span class="value">${e.address||"Non renseign\xE9e"}</span>
              </div>
              <div class="info-item">
                <span class="label">Superficie:</span>
                <span class="value">${e.area?e.area+" m\xB2":"N/A"}</span>
              </div>
              <div class="info-item">
                <span class="label">Zone:</span>
                <span class="value">${e.zone||"Non d\xE9finie"}</span>
              </div>
              <div class="info-item">
                <span class="label">Cat\xE9gorie:</span>
                <span class="value">${e.category||"Non d\xE9finie"}</span>
              </div>
              <div class="info-item">
                <span class="label">Statut:</span>
                <span class="value">${this.getStatusLabel(e.status)}</span>
              </div>
            </div>
          </section>

          ${e.description?`
          <section class="section">
            <h3>Description</h3>
            <p>${e.description}</p>
          </section>
          `:""}

          <!-- Coordinates -->
          ${e.coordinates?.lat&&e.coordinates?.lng?`
          <section class="section">
            <h3>Localisation</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">Latitude:</span>
                <span class="value">${e.coordinates.lat.toFixed(6)}</span>
              </div>
              <div class="info-item">
                <span class="label">Longitude:</span>
                <span class="value">${e.coordinates.lng.toFixed(6)}</span>
              </div>
            </div>
          </section>
          `:""}

          <!-- Owners -->
          ${t.includeOwners&&e.owners&&e.owners.length>0?`
          <section class="section">
            <h3>Propri\xE9taires (${e.owners.length})</h3>
            <table class="owners-table">
              <thead>
                <tr>
                  <th>Nom</th>
                  <th>Type</th>
                  <th>Contact</th>
                  <th>Pourcentage</th>
                </tr>
              </thead>
              <tbody>
                ${e.owners.map(s=>`
                  <tr>
                    <td>${s.name}</td>
                    <td>${this.getOwnershipTypeLabel(s.ownership_type)}</td>
                    <td>${s.contact||"N/A"}</td>
                    <td>${s.ownership_percentage?s.ownership_percentage+"%":"N/A"}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </section>
          `:""}

          <!-- Metadata -->
          <section class="section">
            <h3>M\xE9tadonn\xE9es</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">Date de cr\xE9ation:</span>
                <span class="value">${this.datePipe.transform(e.created_at,"long")}</span>
              </div>
              <div class="info-item">
                <span class="label">Derni\xE8re modification:</span>
                <span class="value">${this.datePipe.transform(e.updated_at,"long")}</span>
              </div>
            </div>
          </section>

          <!-- Footer -->
          <div class="print-footer">
            <p>Document g\xE9n\xE9r\xE9 automatiquement par le Syst\xE8me d'Information Urbaine (SIU)</p>
            <p>Ce document n'a aucune valeur l\xE9gale sans signature officielle</p>
          </div>
        </div>
      </body>
      </html>
    `}generateParcelContent(e,t){return`
      <div class="parcel-title">
        <h2>Parcelle ${e.reference}</h2>
        <span class="status-badge status-${e.status}">
          ${this.getStatusLabel(e.status)}
        </span>
      </div>
      <section class="section">
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Adresse:</span>
            <span class="value">${e.address||"Non renseign\xE9e"}</span>
          </div>
          <div class="info-item">
            <span class="label">Superficie:</span>
            <span class="value">${e.area?e.area+" m\xB2":"N/A"}</span>
          </div>
          <div class="info-item">
            <span class="label">Zone:</span>
            <span class="value">${e.zone||"Non d\xE9finie"}</span>
          </div>
          <div class="info-item">
            <span class="label">Cat\xE9gorie:</span>
            <span class="value">${e.category||"Non d\xE9finie"}</span>
          </div>
        </div>
      </section>
    `}getPrintStyles(){return`
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #333;
      }

      .print-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 40px;
        position: relative;
      }

      .print-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 20px;
        border-bottom: 3px solid #673ab7;
        margin-bottom: 30px;
      }

      .header-left {
        display: flex;
        gap: 15px;
        align-items: center;
      }

      .logo {
        max-width: 80px;
        height: auto;
      }

      .header-text h1 {
        font-size: 18pt;
        font-weight: 600;
        color: #673ab7;
        margin-bottom: 5px;
      }

      .header-text p {
        font-size: 11pt;
        color: #666;
      }

      .header-right {
        text-align: right;
      }

      .qr-code {
        width: 80px;
        height: 80px;
        margin-bottom: 10px;
      }

      .print-date {
        font-size: 9pt;
        color: #666;
      }

      .parcel-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        padding: 15px;
        background-color: #f5f5f5;
        border-radius: 8px;
      }

      .parcel-title h2 {
        font-size: 20pt;
        font-weight: 600;
        color: #333;
      }

      .status-badge {
        padding: 8px 16px;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 10pt;
      }

      .status-available { background-color: #4caf50; }
      .status-occupied { background-color: #2196f3; }
      .status-disputed { background-color: #f44336; }
      .status-reserved { background-color: #ff9800; }

      .section {
        margin-bottom: 30px;
        page-break-inside: avoid;
      }

      .section h3 {
        font-size: 14pt;
        font-weight: 600;
        color: #673ab7;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e0e0e0;
      }

      .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
      }

      .info-item {
        display: flex;
        flex-direction: column;
        gap: 5px;
      }

      .info-item .label {
        font-weight: 600;
        color: #666;
        font-size: 10pt;
      }

      .info-item .value {
        font-size: 11pt;
        color: #333;
      }

      .owners-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
      }

      .owners-table th {
        background-color: #673ab7;
        color: white;
        padding: 10px;
        text-align: left;
        font-weight: 600;
      }

      .owners-table td {
        padding: 10px;
        border-bottom: 1px solid #e0e0e0;
      }

      .owners-table tr:nth-child(even) {
        background-color: #f9f9f9;
      }

      .print-footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 2px solid #e0e0e0;
        text-align: center;
        font-size: 9pt;
        color: #999;
      }

      .print-footer p {
        margin: 5px 0;
      }

      .page-number {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 9pt;
        color: #999;
      }

      @media print {
        body {
          print-color-adjust: exact;
          -webkit-print-color-adjust: exact;
        }

        .print-container {
          padding: 20px;
        }
      }

      @page {
        size: A4;
        margin: 2cm;
      }
    `}generateMultiParcelsHTML(e,t){let i=this.datePipe.transform(new Date,"long");return`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Liste de ${e.length} Parcelles</title>
        <style>
          ${this.getPrintStyles()}
          .parcel-summary {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            page-break-inside: avoid;
          }
          .parcel-summary h3 {
            margin-bottom: 15px;
            color: #673ab7;
          }
        </style>
      </head>
      <body>
        <div class="print-container">
          <div class="print-header">
            <div class="header-left">
              <div class="header-text">
                <h1>Syst\xE8me d'Information Urbaine</h1>
                <p>Liste de Parcelles</p>
              </div>
            </div>
            <div class="header-right">
              <p class="print-date">Imprim\xE9 le ${i}</p>
            </div>
          </div>

          <h2 style="margin-bottom: 30px;">Liste de ${e.length} Parcelles</h2>

          ${e.map(l=>`
            <div class="parcel-summary">
              <h3>${l.reference} - ${this.getStatusLabel(l.status)}</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="label">Adresse:</span>
                  <span class="value">${l.address||"Non renseign\xE9e"}</span>
                </div>
                <div class="info-item">
                  <span class="label">Superficie:</span>
                  <span class="value">${l.area?l.area+" m\xB2":"N/A"}</span>
                </div>
                <div class="info-item">
                  <span class="label">Zone:</span>
                  <span class="value">${l.zone||"Non d\xE9finie"}</span>
                </div>
                <div class="info-item">
                  <span class="label">Cat\xE9gorie:</span>
                  <span class="value">${l.category||"Non d\xE9finie"}</span>
                </div>
              </div>
            </div>
          `).join("")}

          <div class="print-footer">
            <p>Document g\xE9n\xE9r\xE9 automatiquement par le Syst\xE8me d'Information Urbaine (SIU)</p>
          </div>
        </div>
      </body>
      </html>
    `}generateQRCodeDataURL(e){return`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(e)}`}getStatusLabel(e){return{available:"Disponible",occupied:"Occup\xE9",disputed:"Contest\xE9",reserved:"R\xE9serv\xE9"}[e]||e}getOwnershipTypeLabel(e){return{full:"Propri\xE9t\xE9 compl\xE8te",partial:"Propri\xE9t\xE9 partielle",temporary:"Propri\xE9t\xE9 temporaire"}[e]||e}static{this.\u0275fac=function(t){return new(t||n)}}static{this.\u0275prov=A({token:n,factory:n.\u0275fac,providedIn:"root"})}};var ti=n=>["/parcels",n];function ii(n,e){if(n&1&&(a(0,"div",5)(1,"mat-icon",6),r(2,"people"),o(),a(3,"span",7),r(4,"Propri\xE9taires:"),o(),a(5,"span",8),r(6),o()()),n&2){let t=d();c(6),h(t.parcel.owners.length)}}function ni(n,e){if(n&1&&(a(0,"div",5)(1,"mat-icon",6),r(2,"description"),o(),a(3,"span",7),r(4,"Documents:"),o(),a(5,"span",8),r(6),o()()),n&2){let t=d();c(6),h(t.parcel.documents.length)}}function oi(n,e){if(n&1&&(a(0,"mat-chip",16),r(1),T(2,"date"),o()),n&2){let t=d();u("disabled",!0),c(),x(" Cr\xE9\xE9e: ",k(2,2,t.parcel.created_at,"shortDate")," ")}}function ai(n,e){if(n&1&&(a(0,"mat-chip",17),r(1),o()),n&2){let t=d();u("color",t.getStatusColorForChip(t.parcel.status)),c(),x(" ",t.getStatusLabel(t.parcel.status)," ")}}var le=class n{constructor(){this.isSelected=!1;this.viewDetails=new R;this.locateOnMap=new R;this.shareParcel=new R}getStatusColor(e){return e&&{available:"#4caf50",occupied:"#2196f3",disputed:"#f44336",reserved:"#ff9800"}[e]||"#9e9e9e"}getStatusBackgroundColor(e){return this.getStatusColor(e)+"20"}getStatusIcon(e){return e&&{available:"check_circle",occupied:"home",disputed:"warning",reserved:"lock"}[e]||"help_outline"}getStatusLabel(e){return e?{available:"Disponible",occupied:"Occup\xE9",disputed:"Contest\xE9",reserved:"R\xE9serv\xE9"}[e]||e:"Inconnu"}getCategoryColor(e){return e&&{residential:"#3887be",commercial:"#bc3de3",industrial:"#ff8100",agricultural:"#8fa900","mixed-use":"#99008a","public-space":"#007d79",Habitation:"#3887be",CTOM:"#bc3de3",Gendarmerie:"#ff8100",Police:"#007d79",CSPS:"#8fa900",CMA:"#99008a",CEEP:"#bc3de3","Ecole primaire":"#ff8100","Ecole secondaire":"#808080","Enseignement secondaire":"#808080","Complexe scolaire":"#808080","Jardin d'enfants":"#808080",Sante:"#ff0000",Forage:"#0000ff",Fontaine:"#0000ff","Chateau d'eau":"#0000ff",Mosquee:"#00aa00","Eglise catholique":"#800000",Culte:"#800000",Cimetiere:"#a9a9a9","Cimetiere catholique":"#a9a9a9","Lieu sacre":"#800080","Place publique":"#007d79","Jardin public":"#8fa900","Terrain de sport":"#006400","Plateau omnisports":"#006400","Aire de jeux":"#daa520","Aire de stationnement":"#696969","Village traditionnel":"#8b4513","Habitat collectif":"#3887be","Domaine prive":"#800080","Servitude haute tension":"#ffff00","Centre commercial":"#bc3de3","Grand marche":"#bc3de3",Marche:"#bc3de3","Station service":"#ff8c00","Gare routiere":"#708090","Maison de la femme":"#ff69b4","Maison des jeunes":"#4169e1","Association Woroyire":"#20b2aa","Association lolo":"#20b2aa","Groupement Darsalam":"#20b2aa",ZNA:"#ffa500",DT:"#ffa500",RA:"#ffa500",RF:"#ffa500",EV:"#ffa500",Indefini:"#808080"}[e]||"#9e9e9e"}getCategoryLabel(e){return e?{residential:"R\xE9sidentiel",commercial:"Commercial",industrial:"Industriel",agricultural:"Agricole","mixed-use":"Mixte","public-space":"Espace public",Habitation:"Habitation",CTOM:"CTOM",Gendarmerie:"Gendarmerie",Police:"Police",CSPS:"CSPS",CMA:"CMA",CEEP:"CEEP","Ecole primaire":"\xC9cole primaire","Ecole secondaire":"\xC9cole secondaire","Enseignement secondaire":"Enseignement secondaire","Complexe scolaire":"Complexe scolaire","Jardin d'enfants":"Jardin d'enfants",Sante:"Sant\xE9",Forage:"Forage",Fontaine:"Fontaine","Chateau d'eau":"Ch\xE2teau d'eau",Mosquee:"Mosqu\xE9e","Eglise catholique":"\xC9glise catholique",Culte:"Lieu de culte",Cimetiere:"Cimeti\xE8re","Cimetiere catholique":"Cimeti\xE8re catholique","Lieu sacre":"Lieu sacr\xE9","Place publique":"Place publique","Jardin public":"Jardin public","Terrain de sport":"Terrain de sport","Plateau omnisports":"Plateau omnisports","Aire de jeux":"Aire de jeux","Aire de stationnement":"Aire de stationnement","Village traditionnel":"Village traditionnel","Habitat collectif":"Habitat collectif","Domaine prive":"Domaine priv\xE9","Servitude haute tension":"Servitude HT","Centre commercial":"Centre commercial","Grand marche":"Grand march\xE9",Marche:"March\xE9","Station service":"Station service","Gare routiere":"Gare routi\xE8re","Maison de la femme":"Maison de la femme","Maison des jeunes":"Maison des jeunes","Association Woroyire":"Association Woroyire","Association lolo":"Association lolo","Groupement Darsalam":"Groupement Darsalam",ZNA:"ZNA",DT:"DT",RA:"RA",RF:"RF",EV:"EV",Indefini:"Ind\xE9fini"}[e]||e:"Non d\xE9fini"}getStatusColorForChip(e){return e&&{available:"primary",occupied:"accent",disputed:"warn",reserved:"primary"}[e]||"default"}static{this.\u0275fac=function(t){return new(t||n)}}static{this.\u0275cmp=N({type:n,selectors:[["app-parcel-card"]],inputs:{parcel:"parcel",isSelected:"isSelected"},outputs:{viewDetails:"viewDetails",locateOnMap:"locateOnMap",shareParcel:"shareParcel"},decls:44,vars:24,consts:[[1,"parcel-card"],[1,"parcel-reference"],[1,"ref-number"],[1,"status-icon",3,"matTooltip"],[1,"parcel-details"],[1,"detail-item"],[1,"detail-icon"],[1,"detail-label"],[1,"detail-value"],["class","detail-item",4,"ngIf"],[1,"parcel-tags"],[3,"disabled",4,"ngIf"],[3,"color",4,"ngIf"],["align","end"],["mat-button","","color","primary",3,"click","routerLink"],["mat-icon-button","",3,"click","matTooltip"],[3,"disabled"],[3,"color"]],template:function(t,i){t&1&&(a(0,"mat-card",0)(1,"mat-card-header")(2,"mat-card-title")(3,"div",1)(4,"span",2),r(5),o(),a(6,"mat-icon",3),r(7),o()()(),a(8,"mat-card-subtitle"),r(9),o()(),a(10,"mat-card-content")(11,"div",4)(12,"div",5)(13,"mat-icon",6),r(14,"square_foot"),o(),a(15,"span",7),r(16,"Superficie:"),o(),a(17,"span",8),r(18),T(19,"number"),o()(),a(20,"div",5)(21,"mat-icon",6),r(22,"category"),o(),a(23,"span",7),r(24,"Cat\xE9gorie:"),o(),a(25,"span",8),r(26),o()(),g(27,ii,7,1,"div",9)(28,ni,7,1,"div",9),o(),a(29,"div",10)(30,"mat-chip-set"),g(31,oi,3,5,"mat-chip",11)(32,ai,2,2,"mat-chip",12),o()()(),a(33,"mat-card-actions",13)(34,"button",14),_("click",function(){return i.viewDetails.emit(i.parcel)}),a(35,"mat-icon"),r(36,"visibility"),o(),r(37," Voir d\xE9tails "),o(),a(38,"button",15),_("click",function(){return i.locateOnMap.emit(i.parcel)}),a(39,"mat-icon"),r(40,"location_on"),o()(),a(41,"button",15),_("click",function(){return i.shareParcel.emit(i.parcel)}),a(42,"mat-icon"),r(43,"share"),o()()()()),t&2&&($("selected",i.isSelected),c(5),h(i.parcel.reference_cadastrale),c(),E("color",i.getStatusColor(i.parcel.status)),u("matTooltip",i.getStatusLabel(i.parcel.status)),c(),x(" ",i.getStatusIcon(i.parcel.status)," "),c(2),h(i.parcel.address),c(9),x("",k(19,19,i.parcel.area,"1.0-0")," m\xB2"),c(3),E("color",i.getCategoryColor(i.parcel.category)),c(5),h(i.getCategoryLabel(i.parcel.category)),c(),u("ngIf",i.parcel.owners&&i.parcel.owners.length>0),c(),u("ngIf",i.parcel.documents&&i.parcel.documents.length>0),c(3),u("ngIf",i.parcel.created_at),c(),u("ngIf",i.parcel.status),c(2),u("routerLink",Oe(22,ti,i.parcel.id)),c(4),u("matTooltip","Localiser sur la carte"),c(3),u("matTooltip","Partager"))},dependencies:[q,Te,Le,H,G,U,Ye,Ze,We,Qe,Je,Q,Z,J,W,Y,ie,ee,te,X,K,ot,Ue,B,j],styles:[".parcel-card[_ngcontent-%COMP%]{margin:8px;transition:all .2s ease-in-out;border-left:4px solid transparent}.parcel-card[_ngcontent-%COMP%]:hover{transform:translateY(-2px);box-shadow:0 4px 12px #00000026}.parcel-card.selected[_ngcontent-%COMP%]{border-left-color:#1976d2;box-shadow:0 4px 12px #1976d24d}.parcel-reference[_ngcontent-%COMP%]{display:flex;align-items:center;gap:8px}.ref-number[_ngcontent-%COMP%]{font-weight:600;font-size:1.1em}.status-icon[_ngcontent-%COMP%]{font-size:20px;width:20px;height:20px}.parcel-details[_ngcontent-%COMP%]{display:flex;flex-direction:column;gap:8px;margin:12px 0}.detail-item[_ngcontent-%COMP%]{display:flex;align-items:center;gap:8px;font-size:.9em}.detail-icon[_ngcontent-%COMP%]{font-size:16px;width:16px;height:16px;color:#757575}.detail-label[_ngcontent-%COMP%]{color:#757575;min-width:100px}.detail-value[_ngcontent-%COMP%]{font-weight:500;flex:1}.parcel-tags[_ngcontent-%COMP%]{margin-top:12px}@media(max-width:768px){.parcel-card[_ngcontent-%COMP%]{margin:4px}.detail-item[_ngcontent-%COMP%]{flex-wrap:wrap}}"],changeDetection:0})}};var ri=()=>[1,2,3,4,5],li=()=>[5,10,25,50,100],ci=()=>[6,12,24,48],si=()=>[10,25,50,100],Ut=(n,e)=>e.value,di=(n,e)=>e.id;function mi(n,e){if(n&1&&(a(0,"mat-chip",9)(1,"mat-icon"),r(2,"warning"),o(),r(3),o()),n&2){let t=d();c(3),x(" ",t.stats().disputed," contest\xE9es ")}}function pi(n,e){n&1&&(a(0,"button",18)(1,"mat-icon"),r(2,"add"),o(),r(3," Nouvelle parcelle "),o())}function ui(n,e){if(n&1){let t=C();a(0,"button",42),_("click",function(){m(t);let l=d(2);return p(l.deleteSelected())}),a(1,"mat-icon"),r(2,"delete"),o(),r(3," Supprimer "),o()}}function _i(n,e){if(n&1){let t=C();a(0,"mat-card",19)(1,"div",37)(2,"mat-icon"),r(3,"check_circle"),o(),a(4,"span")(5,"strong"),r(6),o(),r(7," parcelle(s) s\xE9lectionn\xE9e(s)"),o()(),a(8,"div",38)(9,"button",39),_("click",function(){m(t);let l=d();return p(l.selection.clear())}),a(10,"mat-icon"),r(11,"clear"),o(),r(12," D\xE9s\xE9lectionner tout "),o(),a(13,"button",39),_("click",function(){m(t);let l=d();return p(l.compareSelected())}),a(14,"mat-icon"),r(15,"compare"),o(),r(16," Comparer "),o(),a(17,"button",39),_("click",function(){m(t);let l=d();return p(l.printSelected())}),a(18,"mat-icon"),r(19,"print"),o(),r(20," Imprimer "),o(),a(21,"button",40)(22,"mat-icon"),r(23,"download"),o(),r(24," Exporter "),o(),a(25,"mat-menu",null,1)(27,"button",17),_("click",function(){m(t);let l=d();return p(l.exportSelected("csv"))}),r(28,"CSV"),o(),a(29,"button",17),_("click",function(){m(t);let l=d();return p(l.exportSelected("excel"))}),r(30,"Excel"),o(),a(31,"button",17),_("click",function(){m(t);let l=d();return p(l.exportSelected("pdf"))}),r(32,"PDF"),o(),a(33,"button",17),_("click",function(){m(t);let l=d();return p(l.exportSelected("json"))}),r(34,"JSON"),o()(),b(35,ui,4,0,"button",41),o()()}if(n&2){let t=ue(26),i=d();u("@fadeIn",void 0),c(6),h(i.selectedCount()),c(15),u("matMenuTriggerFor",t),c(14),v(i.isAdmin()?35:-1)}}function fi(n,e){if(n&1){let t=C();a(0,"button",39),_("click",function(){m(t);let l=d();return p(l.clearFilters())}),a(1,"mat-icon"),r(2,"clear"),o(),r(3," Effacer les filtres "),o()}}function gi(n,e){if(n&1&&(a(0,"mat-option",28)(1,"mat-icon"),r(2),o(),r(3),o()),n&2){let t=e.$implicit;u("value",t.value),c(),E("color",t.color),c(),h(t.icon),c(),x(" ",t.label," ")}}function Ci(n,e){if(n&1&&(a(0,"mat-option",28),r(1),o()),n&2){let t=e.$implicit;u("value",t.value),c(),h(t.label)}}function hi(n,e){n&1&&y(0,"app-skeleton-loader",43)}function xi(n,e){n&1&&(a(0,"div",35),D(1,hi,1,0,"app-skeleton-loader",43,ye),o()),n&2&&(c(),I(F(0,ri)))}function bi(n,e){n&1&&y(0,"app-loading-spinner",36)}function vi(n,e){if(n&1){let t=C();a(0,"th",61)(1,"mat-checkbox",62),_("change",function(l){m(t);let s=d(4);return p(l?s.toggleAllRows():null)}),o()()}if(n&2){let t=d(4);c(),u("checked",t.selection.hasValue()&&t.isAllSelected())("indeterminate",t.selection.hasValue()&&!t.isAllSelected())}}function Si(n,e){if(n&1){let t=C();a(0,"td",63)(1,"mat-checkbox",64),_("click",function(l){return m(t),p(l.stopPropagation())})("change",function(l){let s=m(t).$implicit,f=d(4);return p(l?f.selection.toggle(s):null)}),o()()}if(n&2){let t=e.$implicit,i=d(4);c(),u("checked",i.selection.isSelected(t)),Me("aria-label","S\xE9lectionner "+t.reference)}}function Pi(n,e){n&1&&(a(0,"th",65),r(1,"R\xE9f\xE9rence"),o())}function wi(n,e){n&1&&(a(0,"mat-icon",67),r(1,"star"),o())}function Mi(n,e){if(n&1&&(a(0,"td",63)(1,"div",66)(2,"strong"),r(3),o(),b(4,wi,2,0,"mat-icon",67),o()()),n&2){let t=e.$implicit,i=d(4);c(3),h(t.reference),c(),v(i.isFavorite(t)?4:-1)}}function yi(n,e){n&1&&(a(0,"th",65),r(1,"Adresse"),o())}function Ei(n,e){if(n&1&&(a(0,"td",63),r(1),o()),n&2){let t=e.$implicit;c(),h(t.address||"N/A")}}function Oi(n,e){n&1&&(a(0,"th",65),r(1,"Superficie"),o())}function Ti(n,e){if(n&1&&(a(0,"td",63),r(1),T(2,"number"),o()),n&2){let t=e.$implicit;c(),x(" ",t.area?k(2,1,t.area,"1.0-0")+" m\xB2":"N/A"," ")}}function ki(n,e){n&1&&(a(0,"th",65),r(1,"Zone"),o())}function Li(n,e){if(n&1&&(a(0,"td",63),r(1),o()),n&2){let t=e.$implicit;c(),h(t.zone||"N/A")}}function Di(n,e){n&1&&(a(0,"th",61),r(1,"Cat\xE9gorie"),o())}function Ii(n,e){if(n&1&&(a(0,"td",63)(1,"span",68),r(2),o()()),n&2){let t=e.$implicit,i=d(4);c(),E("background-color",i.getCategoryColor(t.category)),c(),x(" ",i.getCategoryLabel(t.category)," ")}}function $i(n,e){n&1&&(a(0,"th",65),r(1,"Statut"),o())}function Fi(n,e){if(n&1&&(a(0,"td",63)(1,"span",69)(2,"mat-icon"),r(3),o(),r(4),o()()),n&2){let t=e.$implicit,i=d(4);c(),E("background-color",i.getStatusColor(t.status)),c(2),h(i.getStatusIcon(t.status)),c(),x(" ",i.getStatusLabel(t.status)," ")}}function Vi(n,e){n&1&&(a(0,"th",61),r(1,"Actions"),o())}function Ai(n,e){if(n&1){let t=C();a(0,"button",72),_("click",function(){m(t);let l=d().$implicit,s=d(4);return p(s.editParcel(l))}),a(1,"mat-icon"),r(2,"edit"),o()(),a(3,"button",73),_("click",function(){m(t);let l=d().$implicit,s=d(4);return p(s.deleteParcel(l))}),a(4,"mat-icon"),r(5,"delete"),o()()}}function Ri(n,e){if(n&1){let t=C();a(0,"td",63)(1,"button",70),_("click",function(){let l=m(t).$implicit,s=d(4);return p(s.viewParcel(l))}),a(2,"mat-icon"),r(3,"visibility"),o()(),a(4,"button",71),_("click",function(){let l=m(t).$implicit,s=d(4);return p(s.toggleFavorite(l))}),a(5,"mat-icon"),r(6),o()(),b(7,Ai,6,0),o()}if(n&2){let t=e.$implicit,i=d(4);c(4),$("favorite",i.isFavorite(t)),u("matTooltip",i.isFavorite(t)?"Retirer des favoris":"Ajouter aux favoris"),c(2),h(i.isFavorite(t)?"star":"star_border"),c(),v(i.isAdmin()?7:-1)}}function Ni(n,e){n&1&&y(0,"tr",74)}function zi(n,e){if(n&1){let t=C();a(0,"tr",75),_("click",function(){let l=m(t).$implicit,s=d(4);return p(s.viewParcel(l))})("keydown",function(l){let s=m(t).$implicit,f=d(4);return p(f.onKeydown(l,s))}),o()}if(n&2){let t=e.$implicit,i=d(4);$("selected",i.selection.isSelected(t))}}function ji(n,e){if(n&1){let t=C();a(0,"div",45)(1,"table",46),_("matSortChange",function(l){m(t);let s=d(3);return p(s.onSortChange(l))}),S(2,47),g(3,vi,2,2,"th",48)(4,Si,2,2,"td",49),P(),S(5,50),g(6,Pi,2,0,"th",51)(7,Mi,5,2,"td",49),P(),S(8,52),g(9,yi,2,0,"th",51)(10,Ei,2,1,"td",49),P(),S(11,53),g(12,Oi,2,0,"th",51)(13,Ti,3,4,"td",49),P(),S(14,54),g(15,ki,2,0,"th",51)(16,Li,2,1,"td",49),P(),S(17,55),g(18,Di,2,0,"th",48)(19,Ii,3,3,"td",49),P(),S(20,56),g(21,$i,2,0,"th",51)(22,Fi,5,4,"td",49),P(),S(23,57),g(24,Vi,2,0,"th",48)(25,Ri,8,5,"td",49),P(),g(26,Ni,1,0,"tr",58)(27,zi,1,2,"tr",59),o()(),a(28,"mat-paginator",60),_("page",function(l){m(t);let s=d(3);return p(s.onPageChange(l))}),o()}if(n&2){let t=d(3);c(),u("dataSource",t.parcels()),c(25),u("matHeaderRowDef",t.displayedColumns),c(),u("matRowDefColumns",t.displayedColumns),c(),u("length",t.totalParcels())("pageSize",t.pageSize())("pageIndex",t.pageIndex())("pageSizeOptions",F(7,li))}}function Bi(n,e){if(n&1){let t=C();a(0,"app-parcel-card",79),_("viewDetails",function(l){m(t);let s=d(4);return p(s.viewParcel(l))})("locateOnMap",function(l){m(t);let s=d(4);return p(s.viewParcel(l))})("shareParcel",function(l){m(t);let s=d(4);return p(s.toggleFavorite(l))}),o()}if(n&2){let t=e.$implicit,i=d(4);u("parcel",t)("isSelected",i.selection.isSelected(t))}}function qi(n,e){if(n&1){let t=C();a(0,"div",76),D(1,Bi,1,2,"app-parcel-card",77,di),o(),a(3,"mat-paginator",78),_("page",function(l){m(t);let s=d(3);return p(s.onPageChange(l))}),o()}if(n&2){let t=d(3);u("@listAnimation",void 0),c(),I(t.parcels()),c(2),u("length",t.totalParcels())("pageSize",t.pageSize())("pageIndex",t.pageIndex())("pageSizeOptions",F(5,ci))}}function Hi(n,e){n&1&&(a(0,"th",61),r(1,"R\xE9f\xE9rence"),o())}function Ui(n,e){if(n&1&&(a(0,"td",63)(1,"strong"),r(2),o()()),n&2){let t=e.$implicit;c(2),h(t.reference)}}function Gi(n,e){n&1&&(a(0,"th",61),r(1,"Adresse"),o())}function Ji(n,e){if(n&1&&(a(0,"td",63),r(1),o()),n&2){let t=e.$implicit;c(),h(t.address||"N/A")}}function Zi(n,e){n&1&&(a(0,"th",61),r(1,"Superficie"),o())}function Qi(n,e){if(n&1&&(a(0,"td",63),r(1),T(2,"number"),o()),n&2){let t=e.$implicit;c(),x(" ",t.area?k(2,1,t.area,"1.0-0")+" m\xB2":"N/A"," ")}}function Yi(n,e){n&1&&(a(0,"th",61),r(1,"Statut"),o())}function Wi(n,e){if(n&1&&(a(0,"td",63)(1,"mat-icon",83),r(2),o()()),n&2){let t=e.$implicit,i=d(4);c(),E("color",i.getStatusColor(t.status)),u("matTooltip",i.getStatusLabel(t.status)),c(),x(" ",i.getStatusIcon(t.status)," ")}}function Ki(n,e){n&1&&(a(0,"th",61),r(1,"Actions"),o())}function Xi(n,e){if(n&1){let t=C();a(0,"td",63)(1,"button",84),_("click",function(){let l=m(t).$implicit,s=d(4);return p(s.viewParcel(l))}),a(2,"mat-icon"),r(3,"arrow_forward"),o()()()}}function en(n,e){n&1&&y(0,"tr",74)}function tn(n,e){if(n&1){let t=C();a(0,"tr",85),_("click",function(){let l=m(t).$implicit,s=d(4);return p(s.viewParcel(l))}),o()}}function nn(n,e){if(n&1){let t=C();a(0,"div",80)(1,"table",81),S(2,50),g(3,Hi,2,0,"th",48)(4,Ui,3,1,"td",49),P(),S(5,52),g(6,Gi,2,0,"th",48)(7,Ji,2,1,"td",49),P(),S(8,53),g(9,Zi,2,0,"th",48)(10,Qi,3,4,"td",49),P(),S(11,56),g(12,Yi,2,0,"th",48)(13,Wi,3,4,"td",49),P(),S(14,57),g(15,Ki,2,0,"th",48)(16,Xi,4,0,"td",49),P(),g(17,en,1,0,"tr",58)(18,tn,1,0,"tr",82),o()(),a(19,"mat-paginator",78),_("page",function(l){m(t);let s=d(3);return p(s.onPageChange(l))}),o()}if(n&2){let t=d(3);c(),u("dataSource",t.parcels()),c(16),u("matHeaderRowDef",t.compactColumns),c(),u("matRowDefColumns",t.compactColumns),c(),u("length",t.totalParcels())("pageSize",t.pageSize())("pageIndex",t.pageIndex())("pageSizeOptions",F(7,si))}}function on(n,e){if(n&1&&(b(0,ji,29,8),b(1,qi,4,6),b(2,nn,20,8)),n&2){let t=d(2);v(t.viewMode()==="table"?0:-1),c(),v(t.viewMode()==="grid"?1:-1),c(),v(t.viewMode()==="compact"?2:-1)}}function an(n,e){if(n&1){let t=C();a(0,"p"),r(1,"Aucun r\xE9sultat ne correspond \xE0 vos crit\xE8res de recherche."),o(),a(2,"button",86),_("click",function(){m(t);let l=d(3);return p(l.clearFilters())}),a(3,"mat-icon"),r(4,"clear"),o(),r(5," Effacer les filtres "),o()}}function rn(n,e){n&1&&(a(0,"button",18)(1,"mat-icon"),r(2,"add"),o(),r(3," Ajouter une parcelle "),o())}function ln(n,e){if(n&1&&(a(0,"p"),r(1,"Il n'y a pas encore de parcelles enregistr\xE9es."),o(),b(2,rn,4,0,"button",18)),n&2){let t=d(3);c(2),v(t.isAdmin()?2:-1)}}function cn(n,e){if(n&1&&(a(0,"div",44)(1,"mat-icon"),r(2,"inbox"),o(),a(3,"h2"),r(4,"Aucune parcelle trouv\xE9e"),o(),b(5,an,6,0)(6,ln,3,1),o()),n&2){let t=d(2);c(5),v(t.hasFilters()?5:6)}}function sn(n,e){if(n&1&&b(0,on,3,3)(1,cn,7,1,"div",44),n&2){let t=d();v(t.parcels()&&t.parcels().length>0?0:1)}}var Gt=class n{constructor(){this.parcelService=w(Bt);this.authService=w(Fe);this.exportService=w(ae);this.notificationService=w(ft);this.favoritesService=w(qt);this.printService=w(re);this.dialog=w(Vt);this.snackBar=w(rt);this.fb=w(He);this.router=w(ke);this.isAdmin=this.authService.isAdmin;this.loading=M(!1);this.initialLoad=M(!0);this.parcels=M([]);this.totalParcels=M(0);this.pageSize=M(10);this.pageIndex=M(0);this.sortColumn=M("reference");this.sortDirection=M("asc");this.viewMode=M("table");this.hasFilters=z(()=>{let e=this.filterForm.value;return!!(e.reference||e.status||e.zone||e.category||e.minArea||e.maxArea)});this.selectedCount=z(()=>this.selection.selected.length);this.hasSelection=z(()=>this.selectedCount()>0);this.selection=new st(!0,[]);this.showSelectionMode=M(!1);this.searchSubject=new xe;this.displayedColumns=["select","reference","address","area","zone","category","status","actions"];this.compactColumns=["reference","address","area","status","actions"];this.categoryOptions=[{value:"",label:"Toutes les cat\xE9gories"},{value:"residential",label:"R\xE9sidentiel"},{value:"commercial",label:"Commercial"},{value:"industrial",label:"Industriel"},{value:"agricultural",label:"Agricole"},{value:"mixed-use",label:"Mixte"},{value:"public-space",label:"Espace public"},{value:"Habitation",label:"Habitation"},{value:"CTOM",label:"CTOM"},{value:"Gendarmerie",label:"Gendarmerie"},{value:"Police",label:"Police"},{value:"CSPS",label:"CSPS"},{value:"CMA",label:"CMA"},{value:"CEEP",label:"CEEP"},{value:"Ecole primaire",label:"\xC9cole primaire"},{value:"Ecole secondaire",label:"\xC9cole secondaire"},{value:"Sante",label:"Sant\xE9"},{value:"Forage",label:"Forage"},{value:"Mosquee",label:"Mosqu\xE9e"},{value:"Eglise catholique",label:"\xC9glise catholique"},{value:"Cimetiere",label:"Cimeti\xE8re"}];this.filterForm=this.fb.group({reference:[""],status:[""],zone:[""],category:[""],minArea:[null],maxArea:[null]});this.statusOptions=[{value:"",label:"Tous",icon:"filter_list"},{value:"available",label:"Disponible",icon:"check_circle",color:"#4caf50"},{value:"occupied",label:"Occup\xE9",icon:"home",color:"#2196f3"},{value:"disputed",label:"Contest\xE9",icon:"warning",color:"#f44336"},{value:"reserved",label:"R\xE9serv\xE9",icon:"lock",color:"#ff9800"}];this.stats=M({total:0,available:0,occupied:0,disputed:0,reserved:0,totalArea:0});we(()=>{let e=this.viewMode();localStorage.setItem("parcel_view_mode",e)}),this.searchSubject.pipe(se(400),de(),Pe(()=>this.loading.set(!0)),Se(e=>(this.pageIndex.set(0),this.loadParcelsObservable())),ve(e=>(console.error("Search error:",e),this.loading.set(!1),be([])))).subscribe()}ngOnInit(){this.loadPreferences(),this.loadParcels(),this.loadStats(),this.filterForm.valueChanges.pipe(se(500),de((e,t)=>JSON.stringify(e)===JSON.stringify(t))).subscribe(()=>{this.pageIndex.set(0),this.loadParcels()})}loadPreferences(){let e=localStorage.getItem("parcel_filters");if(e)try{let i=JSON.parse(e);this.filterForm.patchValue(i,{emitEvent:!1})}catch(i){console.error("Error loading saved filters:",i)}let t=localStorage.getItem("parcel_view_mode");t&&this.viewMode.set(t)}loadParcelsObservable(){let e=this.filterForm.value,t=O(O(O(O(O(O({page:this.pageIndex()+1,page_size:this.pageSize(),sort_by:this.sortColumn(),sort_order:this.sortDirection()},e.reference&&{reference:e.reference}),e.status&&{status:e.status}),e.zone&&{zone:e.zone}),e.category&&{category:e.category}),e.minArea&&{min_area:e.minArea}),e.maxArea&&{max_area:e.maxArea});return this.parcelService.getParcels(t)}loadParcels(e=0){this.loading.set(!0),this.loadParcelsObservable().subscribe({next:t=>{this.parcels.set(t.items),this.totalParcels.set(t.total),this.loading.set(!1),this.initialLoad.set(!1),this.saveFilters()},error:t=>{this.loading.set(!1),this.initialLoad.set(!1),console.error("Error loading parcels:",t),e<2?(setTimeout(()=>{this.loadParcels(e+1)},1e3*(e+1)),this.snackBar.open(`Erreur de chargement. Nouvelle tentative (${e+1}/2)...`,"Fermer",{duration:2e3})):this.snackBar.open("Impossible de charger les parcelles. V\xE9rifiez votre connexion.","R\xE9essayer",{duration:5e3}).onAction().subscribe(()=>{this.loadParcels(0)})}})}loadStats(){this.parcelService.getParcelStats().subscribe({next:e=>{this.stats.set(e)},error:e=>{console.error("Error loading stats:",e)}})}saveFilters(){let e=this.filterForm.value;localStorage.setItem("parcel_filters",JSON.stringify(e))}onPageChange(e){this.pageIndex.set(e.pageIndex),this.pageSize.set(e.pageSize),this.loadParcels()}onSortChange(e){this.sortColumn.set(e.active),this.sortDirection.set(e.direction||"asc"),this.loadParcels()}changeViewMode(e){this.viewMode.set(e)}toggleSelectionMode(){this.showSelectionMode.set(!this.showSelectionMode()),this.showSelectionMode()||this.selection.clear()}isAllSelected(){let e=this.selection.selected.length,t=this.parcels().length;return e===t&&t>0}toggleAllRows(){this.isAllSelected()?this.selection.clear():this.parcels().forEach(e=>this.selection.select(e))}clearFilters(){this.filterForm.reset({reference:"",status:"",zone:"",category:"",minArea:null,maxArea:null}),localStorage.removeItem("parcel_filters")}viewParcel(e){if(!e||!e.id){this.snackBar.open("Parcelle invalide","Fermer",{duration:3e3});return}this.router.navigate(["/parcels",e.id])}editParcel(e){this.router.navigate(["/parcels",e.id,"edit"])}deleteParcel(e){this.dialog.open(Ce,{data:{title:"Supprimer la parcelle",message:`\xCAtes-vous s\xFBr de vouloir supprimer la parcelle ${e.reference} ?`,confirmText:"Supprimer",confirmColor:"warn"}}).afterClosed().subscribe(i=>{i&&this.parcelService.deleteParcel(e.id).subscribe({next:()=>{this.snackBar.open("Parcelle supprim\xE9e avec succ\xE8s","Fermer",{duration:3e3}),this.loadParcels(),this.loadStats()},error:()=>{this.snackBar.open("Erreur lors de la suppression","Fermer",{duration:3e3})}})})}deleteSelected(){let e=this.selection.selected;if(e.length===0){this.notificationService.warning("Aucune parcelle s\xE9lectionn\xE9e");return}this.dialog.open(Ce,{data:{title:"Supprimer les parcelles",message:`\xCAtes-vous s\xFBr de vouloir supprimer ${e.length} parcelle(s) ?

Cette action est irr\xE9versible.`,confirmText:"Supprimer",confirmColor:"warn"}}).afterClosed().subscribe(i=>{if(i){let l=e.map(s=>this.parcelService.deleteParcel(s.id).toPromise());Promise.all(l).then(()=>{this.snackBar.open(`${e.length} parcelle(s) supprim\xE9e(s)`,"Fermer",{duration:3e3}),this.selection.clear(),this.loadParcels(),this.loadStats()}).catch(()=>{this.snackBar.open("Erreur lors de la suppression","Fermer",{duration:3e3})})}})}toggleFavorite(e){let t=`parcel_${e.id}`;this.favoritesService.toggleFavorite(t);let l=this.favoritesService.isFavorite(t)?"Ajout\xE9 aux favoris":"Retir\xE9 des favoris";this.snackBar.open(l,"Fermer",{duration:2e3})}isFavorite(e){return this.favoritesService.isFavorite(`parcel_${e.id}`)}exportToCSV(){if(this.parcels().length===0){this.notificationService.warning("Aucune donn\xE9e \xE0 exporter");return}this.exportService.exportToCSV(this.parcels(),`parcelles_${this.getTimestamp()}.csv`),this.notificationService.success("Export CSV termin\xE9")}exportToExcel(){if(this.parcels().length===0){this.notificationService.warning("Aucune donn\xE9e \xE0 exporter");return}this.exportService.exportToExcel(this.parcels(),`parcelles_${this.getTimestamp()}.xls`),this.notificationService.success("Export Excel termin\xE9")}exportToPDF(){if(this.parcels().length===0){this.notificationService.warning("Aucune donn\xE9e \xE0 exporter");return}if(this.selectedCount()===1){let e=this.selection.selected[0];this.printService.printParcel(e,{includeOwners:!0,includeDocuments:!0,includeHistory:!0,includeQRCode:!0})}else this.selectedCount()>1?this.printService.printMultipleParcels(this.selection.selected):this.exportService.exportToPDF(this.parcels());this.notificationService.info("Ouverture de la fen\xEAtre d'impression...")}exportToJSON(){if(this.parcels().length===0){this.notificationService.warning("Aucune donn\xE9e \xE0 exporter");return}this.exportService.exportToJSON(this.parcels(),`parcelles_${this.getTimestamp()}.json`),this.notificationService.success("Export JSON termin\xE9")}exportStatistics(){if(this.parcels().length===0){this.notificationService.warning("Aucune donn\xE9e \xE0 exporter");return}this.exportService.exportStatistics(this.parcels(),`statistiques_${this.getTimestamp()}.txt`),this.notificationService.success("Export des statistiques termin\xE9")}exportSelected(e){let t=this.selection.selected;if(t.length===0){this.notificationService.warning("Aucune parcelle s\xE9lectionn\xE9e");return}switch(e){case"csv":this.exportService.exportToCSV(t,`parcelles_selection_${this.getTimestamp()}.csv`);break;case"excel":this.exportService.exportToExcel(t,`parcelles_selection_${this.getTimestamp()}.xls`);break;case"pdf":this.exportService.exportToPDF(t);break;case"json":this.exportService.exportToJSON(t,`parcelles_selection_${this.getTimestamp()}.json`);break}this.notificationService.success(`Export de ${t.length} parcelle(s) termin\xE9`)}getTimestamp(){return new Date().toISOString().slice(0,19).replace(/[:-]/g,"").replace("T","_")}getStatusLabel(e){return e?this.statusOptions.find(i=>i.value===e)?.label||e:"Non d\xE9fini"}getStatusColor(e){return e&&this.statusOptions.find(i=>i.value===e)?.color||"#9e9e9e"}getStatusIcon(e){return e&&this.statusOptions.find(i=>i.value===e)?.icon||"help_outline"}getCategoryLabel(e){return e?this.categoryOptions.find(i=>i.value===e)?.label||e:"Non d\xE9fini"}getCategoryColor(e){return e&&{residential:"#3887be",commercial:"#bc3de3",industrial:"#ff8100",agricultural:"#8fa900","mixed-use":"#99008a","public-space":"#007d79",Habitation:"#3887be",CTOM:"#bc3de3",Gendarmerie:"#ff8100",Police:"#007d79",CSPS:"#8fa900"}[e]||"#9e9e9e"}onKeydown(e,t){(e.key==="Enter"||e.key===" ")&&(e.preventDefault(),this.viewParcel(t))}refresh(){this.parcelService.clearCache(),this.loadParcels(),this.loadStats(),this.snackBar.open("Liste actualis\xE9e","OK",{duration:2e3})}compareSelected(){let e=this.selection.selected;if(e.length<2){this.notificationService.warning("Veuillez s\xE9lectionner au moins 2 parcelles pour comparer");return}if(e.length>4){this.notificationService.warning("Maximum 4 parcelles peuvent \xEAtre compar\xE9es");return}let t=e.map(i=>i.id).join(",");this.router.navigate(["/parcels/compare"],{queryParams:{ids:t}})}printSelected(){let e=this.selection.selected;if(e.length===0){this.notificationService.warning("Aucune parcelle s\xE9lectionn\xE9e");return}e.length===1?this.printService.printParcel(e[0],{includeOwners:!0,includeDocuments:!0,includeHistory:!0,includeQRCode:!0}):this.printService.printMultipleParcels(e)}static{this.\u0275fac=function(t){return new(t||n)}}static{this.\u0275cmp=N({type:n,selectors:[["app-parcel-list"]],viewQuery:function(t,i){if(t&1&&Ee(ne,5)(oe,5),t&2){let l;me(l=pe())&&(i.paginator=l.first),me(l=pe())&&(i.sort=l.first)}},decls:116,vars:14,consts:[["exportMenu","matMenu"],["exportSelectedMenu","matMenu"],[1,"parcel-list-container"],[1,"header"],[1,"header-content"],[1,"stats-chips"],[3,"highlighted"],[1,"stat-chip","available"],[1,"stat-chip","occupied"],[1,"stat-chip","disputed"],[1,"header-actions"],["aria-label","Mode d'affichage",3,"change","value"],["value","table","matTooltip","Vue tableau"],["value","grid","matTooltip","Vue grille"],["value","compact","matTooltip","Vue compacte"],["mat-icon-button","","matTooltip","Actualiser",3,"click"],["mat-button","",3,"matMenuTriggerFor","disabled"],["mat-menu-item","",3,"click"],["mat-raised-button","","color","primary","routerLink","/parcels/new"],[1,"selection-bar"],[1,"filters-card"],[1,"filters-header"],["mat-button",""],[1,"filters-form",3,"formGroup"],["appearance","outline"],["matInput","","formControlName","reference","placeholder","Ex: PAR-001"],["matPrefix",""],["formControlName","status"],[3,"value"],["matInput","","formControlName","zone","placeholder","Ex: Zone A"],["formControlName","category"],["appearance","outline",1,"area-field"],["matInput","","type","number","formControlName","minArea","placeholder","0","min","0"],["matInput","","type","number","formControlName","maxArea","placeholder","10000","min","0"],[1,"content-card"],[1,"skeleton-container"],["message","Chargement des parcelles..."],[1,"selection-info"],[1,"selection-actions"],["mat-button","",3,"click"],["mat-button","",3,"matMenuTriggerFor"],["mat-button","","color","warn"],["mat-button","","color","warn",3,"click"],["variant","list"],[1,"empty-state"],[1,"table-container"],["mat-table","","matSort","",1,"parcels-table",3,"matSortChange","dataSource"],["matColumnDef","select"],["mat-header-cell","",4,"matHeaderCellDef"],["mat-cell","",4,"matCellDef"],["matColumnDef","reference"],["mat-header-cell","","mat-sort-header","",4,"matHeaderCellDef"],["matColumnDef","address"],["matColumnDef","area"],["matColumnDef","zone"],["matColumnDef","category"],["matColumnDef","status"],["matColumnDef","actions"],["mat-header-row","",4,"matHeaderRowDef"],["mat-row","","class","table-row","tabindex","0","role","button",3,"selected","click","keydown",4,"matRowDef","matRowDefColumns"],["showFirstLastButtons","","aria-label","S\xE9lection de page",3,"page","length","pageSize","pageIndex","pageSizeOptions"],["mat-header-cell",""],["aria-label","S\xE9lectionner tout",3,"change","checked","indeterminate"],["mat-cell",""],[3,"click","change","checked","aria-label"],["mat-header-cell","","mat-sort-header",""],[1,"cell-reference"],[1,"favorite-icon"],[1,"category-badge"],[1,"status-badge"],["mat-icon-button","","matTooltip","Voir les d\xE9tails",3,"click"],["mat-icon-button","",3,"click","matTooltip"],["mat-icon-button","","matTooltip","Modifier",3,"click"],["mat-icon-button","","matTooltip","Supprimer","color","warn",3,"click"],["mat-header-row",""],["mat-row","","tabindex","0","role","button",1,"table-row",3,"click","keydown"],[1,"grid-container"],[3,"parcel","isSelected"],["showFirstLastButtons","",3,"page","length","pageSize","pageIndex","pageSizeOptions"],[3,"viewDetails","locateOnMap","shareParcel","parcel","isSelected"],[1,"compact-container"],["mat-table","",1,"compact-table",3,"dataSource"],["mat-row","","class","compact-row",3,"click",4,"matRowDef","matRowDefColumns"],[3,"matTooltip"],["mat-icon-button","",3,"click"],["mat-row","",1,"compact-row",3,"click"],["mat-raised-button","",3,"click"]],template:function(t,i){if(t&1){let l=C();a(0,"div",2)(1,"div",3)(2,"div",4)(3,"h1"),r(4,"Gestion des parcelles"),o(),a(5,"div",5)(6,"mat-chip-set")(7,"mat-chip",6)(8,"mat-icon"),r(9,"inventory"),o(),r(10),o(),a(11,"mat-chip",7)(12,"mat-icon"),r(13,"check_circle"),o(),r(14),o(),a(15,"mat-chip",8)(16,"mat-icon"),r(17,"home"),o(),r(18),o(),b(19,mi,4,1,"mat-chip",9),o()()(),a(20,"div",10)(21,"mat-button-toggle-group",11),_("change",function(f){return m(l),p(i.changeViewMode(f.value))}),a(22,"mat-button-toggle",12)(23,"mat-icon"),r(24,"table_rows"),o()(),a(25,"mat-button-toggle",13)(26,"mat-icon"),r(27,"grid_view"),o()(),a(28,"mat-button-toggle",14)(29,"mat-icon"),r(30,"view_list"),o()()(),a(31,"button",15),_("click",function(){return m(l),p(i.refresh())}),a(32,"mat-icon"),r(33,"refresh"),o()(),a(34,"button",16)(35,"mat-icon"),r(36,"download"),o(),r(37," Exporter "),o(),a(38,"mat-menu",null,0)(40,"button",17),_("click",function(){return m(l),p(i.exportToCSV())}),a(41,"mat-icon"),r(42,"table_chart"),o(),a(43,"span"),r(44,"Export CSV"),o()(),a(45,"button",17),_("click",function(){return m(l),p(i.exportToExcel())}),a(46,"mat-icon"),r(47,"description"),o(),a(48,"span"),r(49,"Export Excel"),o()(),a(50,"button",17),_("click",function(){return m(l),p(i.exportToPDF())}),a(51,"mat-icon"),r(52,"picture_as_pdf"),o(),a(53,"span"),r(54,"Export PDF"),o()(),a(55,"button",17),_("click",function(){return m(l),p(i.exportToJSON())}),a(56,"mat-icon"),r(57,"code"),o(),a(58,"span"),r(59,"Export JSON"),o()(),y(60,"mat-divider"),a(61,"button",17),_("click",function(){return m(l),p(i.exportStatistics())}),a(62,"mat-icon"),r(63,"analytics"),o(),a(64,"span"),r(65,"Statistiques"),o()()(),b(66,pi,4,0,"button",18),o()(),b(67,_i,36,4,"mat-card",19),a(68,"mat-card",20)(69,"div",21)(70,"h3")(71,"mat-icon"),r(72,"filter_list"),o(),r(73," Filtres "),o(),b(74,fi,4,0,"button",22),o(),a(75,"form",23)(76,"mat-form-field",24)(77,"mat-label"),r(78,"Rechercher par r\xE9f\xE9rence"),o(),y(79,"input",25),a(80,"mat-icon",26),r(81,"search"),o()(),a(82,"mat-form-field",24)(83,"mat-label"),r(84,"Statut"),o(),a(85,"mat-select",27),D(86,gi,4,5,"mat-option",28,Ut),o()(),a(88,"mat-form-field",24)(89,"mat-label"),r(90,"Zone"),o(),y(91,"input",29),a(92,"mat-icon",26),r(93,"location_city"),o()(),a(94,"mat-form-field",24)(95,"mat-label"),r(96,"Cat\xE9gorie"),o(),a(97,"mat-select",30),D(98,Ci,2,2,"mat-option",28,Ut),o()(),a(100,"mat-form-field",31)(101,"mat-label"),r(102,"Superficie min (m\xB2)"),o(),y(103,"input",32),a(104,"mat-icon",26),r(105,"square_foot"),o()(),a(106,"mat-form-field",31)(107,"mat-label"),r(108,"Superficie max (m\xB2)"),o(),y(109,"input",33),a(110,"mat-icon",26),r(111,"square_foot"),o()()()(),a(112,"mat-card",34),b(113,xi,3,1,"div",35)(114,bi,1,0,"app-loading-spinner",36)(115,sn,2,1),o()()}if(t&2){let l=ue(39);c(5),u("@fadeIn",void 0),c(2),u("highlighted",!0),c(3),x(" ",i.stats().total," parcelles "),c(4),x(" ",i.stats().available," disponibles "),c(4),x(" ",i.stats().occupied," occup\xE9es "),c(),v(i.stats().disputed>0?19:-1),c(2),u("value",i.viewMode()),c(13),u("matMenuTriggerFor",l)("disabled",i.parcels().length===0),c(32),v(i.isAdmin()?66:-1),c(),v(i.hasSelection()?67:-1),c(7),v(i.hasFilters()?74:-1),c(),u("formGroup",i.filterForm),c(11),I(i.statusOptions),c(12),I(i.categoryOptions),c(15),v(i.initialLoad()&&i.loading()?113:i.loading()?114:115)}},dependencies:[q,H,Ge,Ne,Ve,ze,Ae,Re,qe,Be,je,kt,bt,St,yt,Pt,vt,Et,wt,Mt,Ot,Tt,Lt,ne,It,oe,Dt,Ft,$t,Q,Z,J,W,Y,nt,it,et,Ke,Xe,tt,ht,Ct,gt,G,U,At,ut,mt,dt,pt,ct,lt,X,K,_t,zt,Rt,Nt,jt,ie,ee,te,at,xt,Ht,le,B],styles:[".parcel-list-container[_ngcontent-%COMP%]{max-width:1600px;margin:0 auto;padding:1rem}@media(max-width:768px){.parcel-list-container[_ngcontent-%COMP%]{padding:.5rem}}.header[_ngcontent-%COMP%]{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:2rem;gap:1rem;flex-wrap:wrap}.header[_ngcontent-%COMP%]   .header-content[_ngcontent-%COMP%]{flex:1}.header[_ngcontent-%COMP%]   .header-content[_ngcontent-%COMP%]   h1[_ngcontent-%COMP%]{margin:0 0 1rem;font-size:2rem;font-weight:500}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]{margin-top:.5rem}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]   mat-chip-set[_ngcontent-%COMP%]{display:flex;flex-wrap:wrap;gap:.5rem}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]   mat-chip[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.25rem;font-weight:500}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]   mat-chip[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:18px;width:18px;height:18px}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]   mat-chip.stat-chip.available[_ngcontent-%COMP%]{background-color:#4caf501a;color:#4caf50}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]   mat-chip.stat-chip.occupied[_ngcontent-%COMP%]{background-color:#2196f31a;color:#2196f3}.header[_ngcontent-%COMP%]   .stats-chips[_ngcontent-%COMP%]   mat-chip.stat-chip.disputed[_ngcontent-%COMP%]{background-color:#f443361a;color:#f44336}.header[_ngcontent-%COMP%]   .header-actions[_ngcontent-%COMP%]{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}.header[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.5rem}@media(max-width:768px){.header[_ngcontent-%COMP%]{flex-direction:column}.header[_ngcontent-%COMP%]   .header-actions[_ngcontent-%COMP%]{width:100%;justify-content:space-between}}.selection-bar[_ngcontent-%COMP%]{margin-bottom:1rem;padding:1rem;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem}.selection-bar[_ngcontent-%COMP%]   .selection-info[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.5rem}.selection-bar[_ngcontent-%COMP%]   .selection-info[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#fff}.selection-bar[_ngcontent-%COMP%]   .selection-actions[_ngcontent-%COMP%]{display:flex;gap:.5rem;flex-wrap:wrap}.selection-bar[_ngcontent-%COMP%]   .selection-actions[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{color:#fff}.selection-bar[_ngcontent-%COMP%]   .selection-actions[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#fff}.filters-card[_ngcontent-%COMP%]{margin-bottom:1.5rem}.filters-card[_ngcontent-%COMP%]   .filters-header[_ngcontent-%COMP%]{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}.filters-card[_ngcontent-%COMP%]   .filters-header[_ngcontent-%COMP%]   h3[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.5rem;margin:0;font-size:1.1rem;font-weight:500}.filters-form[_ngcontent-%COMP%]{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;align-items:start}.filters-form[_ngcontent-%COMP%]   mat-form-field[_ngcontent-%COMP%]{width:100%}.filters-form[_ngcontent-%COMP%]   .area-field[_ngcontent-%COMP%]{min-width:150px}@media(max-width:768px){.filters-form[_ngcontent-%COMP%]{grid-template-columns:1fr}}.content-card[_ngcontent-%COMP%]{min-height:400px}.skeleton-container[_ngcontent-%COMP%]{display:flex;flex-direction:column;gap:1rem;padding:1rem}.table-container[_ngcontent-%COMP%]{overflow-x:auto}.parcels-table[_ngcontent-%COMP%]{width:100%}.parcels-table[_ngcontent-%COMP%]   .cell-reference[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.5rem}.parcels-table[_ngcontent-%COMP%]   .cell-reference[_ngcontent-%COMP%]   .favorite-icon[_ngcontent-%COMP%]{color:#ffc107;font-size:16px;width:16px;height:16px}.parcels-table[_ngcontent-%COMP%]   .status-badge[_ngcontent-%COMP%]{display:inline-flex;align-items:center;gap:.25rem;padding:.25rem .75rem;border-radius:16px;color:#fff;font-size:.75rem;font-weight:500;white-space:nowrap}.parcels-table[_ngcontent-%COMP%]   .status-badge[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:14px;width:14px;height:14px}.parcels-table[_ngcontent-%COMP%]   .category-badge[_ngcontent-%COMP%]{display:inline-block;padding:.25rem .75rem;border-radius:12px;color:#fff;font-size:.75rem;font-weight:500;white-space:nowrap}.parcels-table[_ngcontent-%COMP%]   .table-row[_ngcontent-%COMP%]{cursor:pointer;transition:background-color .2s}.parcels-table[_ngcontent-%COMP%]   .table-row[_ngcontent-%COMP%]:hover{background-color:#0000000a}.parcels-table[_ngcontent-%COMP%]   .table-row.selected[_ngcontent-%COMP%]{background-color:#673ab714}.parcels-table[_ngcontent-%COMP%]   .table-row[_ngcontent-%COMP%]:focus{outline:2px solid #673ab7;outline-offset:-2px}.parcels-table[_ngcontent-%COMP%]   button.favorite[_ngcontent-%COMP%]{color:#ffc107}.grid-container[_ngcontent-%COMP%]{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.5rem;padding:1rem}@media(max-width:768px){.grid-container[_ngcontent-%COMP%]{grid-template-columns:1fr;gap:1rem}}.compact-container[_ngcontent-%COMP%]{overflow-x:auto}.compact-table[_ngcontent-%COMP%]{width:100%}.compact-table[_ngcontent-%COMP%]   .compact-row[_ngcontent-%COMP%]{cursor:pointer;transition:background-color .2s}.compact-table[_ngcontent-%COMP%]   .compact-row[_ngcontent-%COMP%]:hover{background-color:#0000000a}.compact-table[_ngcontent-%COMP%]   td[_ngcontent-%COMP%], .compact-table[_ngcontent-%COMP%]   th[_ngcontent-%COMP%]{padding:.5rem!important}.empty-state[_ngcontent-%COMP%]{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4rem 2rem;text-align:center}.empty-state[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{font-size:5rem;width:5rem;height:5rem;color:#00000042;margin-bottom:1.5rem}.empty-state[_ngcontent-%COMP%]   h2[_ngcontent-%COMP%]{margin:0 0 .5rem;font-size:1.5rem;font-weight:400;color:#000000b3}.empty-state[_ngcontent-%COMP%]   p[_ngcontent-%COMP%]{margin:0 0 2rem;color:#0009;max-width:400px}.empty-state[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{display:flex;align-items:center;gap:.5rem}mat-paginator[_ngcontent-%COMP%]{background:transparent;border-top:1px solid rgba(0,0,0,.12)}@keyframes _ngcontent-%COMP%_shimmer{0%{background-position:-468px 0}to{background-position:468px 0}}[_ngcontent-%COMP%]:focus-visible{outline:2px solid #673ab7;outline-offset:2px}@media(prefers-color-scheme:dark){.table-row[_ngcontent-%COMP%]:hover{background-color:#ffffff14}.empty-state[_ngcontent-%COMP%]   mat-icon[_ngcontent-%COMP%]{color:#ffffff4d}.empty-state[_ngcontent-%COMP%]   h2[_ngcontent-%COMP%]{color:#ffffffde}.empty-state[_ngcontent-%COMP%]   p[_ngcontent-%COMP%]{color:#fff9}}@media print{.header-actions[_ngcontent-%COMP%], .selection-bar[_ngcontent-%COMP%], .filters-card[_ngcontent-%COMP%], mat-paginator[_ngcontent-%COMP%], button[_ngcontent-%COMP%], mat-checkbox[_ngcontent-%COMP%]{display:none!important}.parcels-table[_ngcontent-%COMP%]{page-break-inside:auto}.parcels-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]{page-break-inside:avoid;page-break-after:auto}}"],data:{animation:[_e("listAnimation",[ge("* => *",[De(":enter",[V({opacity:0,transform:"scale(0.95) translateY(10px)"}),Ie("60ms",[fe("350ms cubic-bezier(0.0, 0.0, 0.2, 1)",V({opacity:1,transform:"scale(1) translateY(0)"}))])],{optional:!0})])]),_e("fadeIn",[ge(":enter",[V({opacity:0}),fe("300ms ease-in",V({opacity:1}))])])]},changeDetection:0})}};export{Gt as ParcelListComponent};
