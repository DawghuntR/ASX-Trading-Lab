You have been tasked with completing an action involving the RIBCX (also known as RIB CX) platform. The following contains details about RIB CX and the APIs available for the platform.

# RIB CX

RIB CX by RIB Software is a cutting-edge cloud-based construction project management platform designed to streamline and optimize the entire construction lifecycle, from initial planning and budgeting to execution and handover. It enables real-time collaboration among stakeholders, integrates advanced cost control, scheduling, and document management features, and leverages AI-driven analytics to improve decision-making and project transparency. RIB CX is particularly useful for large-scale infrastructure and building projects where coordination, cost efficiency, and risk management are critical to success, making it an essential tool for contractors, owners, and project managers aiming to deliver projects on time and within budget.

# RIB CX API Documentation (v25.04)

Base URL: `https://au2.itwocx.com/api/25.04`

## Authentication

The API uses API Key authentication. Include your API key in the header:

-   Header Name: `apiKey`
-   Location: Header

## Available APIs

### 1. Annotation APIs

#### Get Annotations by Revision IDs

-   **GET** `/Api/{project}/Annotation/GetByRevisionIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Revision IDs
    -   `layerIds` (array[int64], required): Layer IDs
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** Array of AnnotationDto objects

#### Get Annotated Revision PDF

-   **GET** `/Api/{project}/Annotation/GetAnnotatedRevisionPdf`
-   **Parameters:**
    -   `revisionId` (int32, required): Revision ID
    -   `layerIds` (array[int32], optional): Layer IDs to include
    -   `layerTypes` (array[string], optional): Layer types to include
    -   `project` (string, required): Project identifier
-   **Response:** PDF file as byte stream

#### Add Annotation to Revision

-   **POST** `/Api/{project}/Annotation/AddToRevision/{id}`
-   **Parameters:**
    -   `id` (int32, required): Revision ID
    -   `annotation` (AnnotationDto, required): Annotation data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 2. Attachment APIs

#### Download Attachment

-   **GET** `/Api/{project}/Attachment/Download/{id}`
-   **Parameters:**
    -   `id` (int32, required): Attachment ID
    -   `chunkId` (int32, optional): Chunk ID for chunked downloads
    -   `project` (string, required): Project identifier
-   **Response:** FileChunkDto object

#### Download Attachment File

-   **GET** `/Api/{project}/Attachment/DownloadFile/{id}`
-   **Parameters:**
    -   `id` (int32, required): Attachment ID
    -   `project` (string, required): Project identifier
-   **Response:** File as byte stream

#### Upload Attachment

-   **POST** `/Api/{project}/Attachment/Upload`
-   **Parameters:**
    -   `documentId` (int64, required): Document ID
    -   `fileUpload` (FileChunkDto, required): File data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Retire Attachment

-   **DELETE** `/Api/{project}/Attachment/Retire/{id}`
-   **Parameters:**
    -   `id` (int32, required): Attachment ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 3. Bidder APIs

#### Get Bidders

-   **GET** `/Api/{project}/Bidder/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `tenderDatabaseId` (int32, optional): Tender database ID
    -   `includeRetired` (boolean, optional): Include retired records
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[BidderDto] with paginated bidder list

#### Get Bidder by ID

-   **GET** `/Api/{project}/Bidder/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Bidder ID
    -   `project` (string, required): Project identifier
-   **Response:** BidderDto object

#### Get Bidders by IDs

-   **GET** `/Api/{project}/Bidder/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of bidder IDs
    -   `tenderDatabaseId` (int32, optional): Tender database ID
    -   `project` (string, required): Project identifier
-   **Response:** Array of BidderDto objects

#### Create Bidder

-   **POST** `/Api/{project}/Bidder/Create`
-   **Parameters:**
    -   `model` (BidderDto, required): Bidder data
    -   `tenderDatabaseId` (int32, optional): Tender database ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Update Bidder

-   **PUT** `/Api/{project}/Bidder/Update`
-   **Parameters:**
    -   `model` (BidderDto, required): Updated bidder data
    -   `tenderDatabaseId` (int32, optional): Tender database ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Upsert Bidder

-   **PUT** `/Api/{project}/Bidder/Upsert`
-   **Parameters:**
    -   `model` (BidderDto, required): Bidder data
    -   `tenderDatabaseId` (int32, optional): Tender database ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 4. Bidder Submission APIs

#### Get Bidder Submissions

-   **GET** `/Api/{project}/BidderSubmission/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[BidderSubmissionDto]

#### Get Bidder Submission by ID

-   **GET** `/Api/{project}/BidderSubmission/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Submission ID
    -   `project` (string, required): Project identifier
-   **Response:** BidderSubmissionDto object

#### Get Bidder Submissions by IDs

-   **GET** `/Api/{project}/BidderSubmission/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of submission IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of BidderSubmissionDto objects

### 5. Budget APIs

#### Get Budgets

-   **GET** `/Api/{project}/Budget/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[BudgetDto]

#### Get Budget by ID

-   **GET** `/Api/{project}/Budget/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Budget ID
    -   `project` (string, required): Project identifier
-   **Response:** BudgetDto object

#### Get Budgets by IDs

-   **GET** `/Api/{project}/Budget/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of budget IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of BudgetDto objects

#### Get Budget by Line Item ID

-   **GET** `/Api/{project}/Budget/GetByLineItemId`
-   **Parameters:**
    -   `lineItemId` (int64, required): Line item ID
    -   `project` (string, required): Project identifier
-   **Response:** BudgetDto object

#### Get Line Item by ID

-   **GET** `/Api/{project}/Budget/GetLineItemById`
-   **Parameters:**
    -   `lineItemId` (int64, required): Line item ID
    -   `project` (string, required): Project identifier
-   **Response:** NumberInfoDto object

#### Get Line Item PDF File

-   **GET** `/Api/{project}/Budget/GetLineItemPdfFile`
-   **Parameters:**
    -   `lineItemId` (int64, required): Line item ID
    -   `project` (string, required): Project identifier
-   **Response:** PDF file as byte stream

#### Create Budget

-   **POST** `/Api/{project}/Budget/Create`
-   **Parameters:**
    -   `model` (BudgetDto, required): Budget data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Budget

-   **DELETE** `/Api/{project}/Budget/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Budget ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 6. Budget Forecast APIs

#### Get Budget Forecasts

-   **GET** `/Api/{project}/BudgetForecast/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[BudgetForecastDto]

#### Get Budget Forecast by ID

-   **GET** `/Api/{project}/BudgetForecast/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Forecast ID
    -   `project` (string, required): Project identifier
-   **Response:** BudgetForecastDto object

#### Get Budget Forecasts by IDs

-   **GET** `/Api/{project}/BudgetForecast/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of forecast IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of BudgetForecastDto objects

#### Create Budget Forecast

-   **POST** `/Api/{project}/BudgetForecast/Create`
-   **Parameters:**
    -   `model` (BudgetForecastDto, required): Forecast data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Update Budget Forecast

-   **PUT** `/Api/{project}/BudgetForecast/Update`
-   **Parameters:**
    -   `model` (BudgetForecastDto, required): Updated forecast data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Budget Forecast

-   **DELETE** `/Api/{project}/BudgetForecast/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Forecast ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 7. Budget Transfer APIs

#### Get Budget Transfers

-   **GET** `/Api/{project}/BudgetTransfer/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[BudgetTransferDto]

#### Get Budget Transfer by ID

-   **GET** `/Api/{project}/BudgetTransfer/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Transfer ID
    -   `project` (string, required): Project identifier
-   **Response:** BudgetTransferDto object

#### Get Budget Transfers by IDs

-   **GET** `/Api/{project}/BudgetTransfer/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of transfer IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of BudgetTransferDto objects

#### Create Budget Transfer

-   **POST** `/Api/{project}/BudgetTransfer/Create`
-   **Parameters:**
    -   `model` (BudgetTransferDto, required): Transfer data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Delete Budget Transfer

-   **DELETE** `/Api/{project}/BudgetTransfer/Delete/{id}`
-   **Parameters:**
    -   `id` (int32, required): Transfer ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 8. Budget Variation APIs

#### Get Budget Variations

-   **GET** `/Api/{project}/BudgetVariation/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[BudgetVariationDto]

#### Get Budget Variation by ID

-   **GET** `/Api/{project}/BudgetVariation/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Variation ID
    -   `project` (string, required): Project identifier
-   **Response:** BudgetVariationDto object

#### Get Budget Variations by IDs

-   **GET** `/Api/{project}/BudgetVariation/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of variation IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of BudgetVariationDto objects

#### Create Budget Variation

-   **POST** `/Api/{project}/BudgetVariation/Create`
-   **Parameters:**
    -   `model` (BudgetVariationDto, required): Variation data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Budget Variation

-   **DELETE** `/Api/{project}/BudgetVariation/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Variation ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 9. Claim APIs

#### Get Claims

-   **GET** `/Api/{project}/Claim/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[ClaimDto]

#### Get Claim by ID

-   **GET** `/Api/{project}/Claim/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Claim ID
    -   `project` (string, required): Project identifier
-   **Response:** ClaimDto object

#### Get Claims by IDs

-   **GET** `/Api/{project}/Claim/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of claim IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of ClaimDto objects

#### Create Claim

-   **POST** `/Api/{project}/Claim/Create`
-   **Parameters:**
    -   `model` (ClaimDto, required): Claim data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Claim

-   **DELETE** `/Api/{project}/Claim/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Claim ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 10. Company APIs

#### Get Companies

-   **GET** `/Api/{project}/Company/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired companies
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[CompanyDto]

#### Get Company by ID

-   **GET** `/Api/{project}/Company/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Company ID
    -   `project` (string, required): Project identifier
-   **Response:** CompanyDto object

#### Get Company by Code

-   **GET** `/Api/{project}/Company/GetByCode`
-   **Parameters:**
    -   `code` (string, required): Company code
    -   `project` (string, required): Project identifier
-   **Response:** CompanyDto object

#### Get Company Roles

-   **GET** `/Api/{project}/Company/GetRoles`
-   **Parameters:**
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired roles
    -   `project` (string, required): Project identifier
-   **Response:** Array of CompanyRoleDto objects

#### Create Company

-   **POST** `/Api/{project}/Company/Create`
-   **Parameters:**
    -   `model` (CompanyDto, required): Company data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Update Company

-   **PUT** `/Api/{project}/Company/Update`
-   **Parameters:**
    -   `model` (CompanyDto, required): Updated company data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Rename Company

-   **PUT** `/Api/{project}/Company/Rename/{id}`
-   **Parameters:**
    -   `id` (int32, required): Company ID
    -   `newCompanyCode` (string, required): New company code
    -   `updatePreferCode` (boolean, optional): Update preferred code
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Restore Company

-   **PATCH** `/Api/{project}/Company/Restore/{id}`
-   **Parameters:**
    -   `id` (int32, required): Company ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Retire Company

-   **DELETE** `/Api/{project}/Company/Retire/{id}`
-   **Parameters:**
    -   `id` (int32, required): Company ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 11. Contract APIs

#### Get Contracts

-   **GET** `/Api/{project}/Contract/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeWithdrawn` (boolean, optional): Include withdrawn contracts
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[ContractDto]

#### Get Contract by ID

-   **GET** `/Api/{project}/Contract/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Contract ID
    -   `project` (string, required): Project identifier
-   **Response:** ContractDto object

#### Get Contracts by IDs

-   **GET** `/Api/{project}/Contract/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of contract IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of ContractDto objects

#### Create Contract

-   **POST** `/Api/{project}/Contract/Create`
-   **Parameters:**
    -   `model` (ContractDto, required): Contract data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Update Contract

-   **PUT** `/Api/{project}/Contract/Update`
-   **Parameters:**
    -   `model` (ContractDto, required): Updated contract data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Contract

-   **DELETE** `/Api/{project}/Contract/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Contract ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 12. Contract Variation APIs

#### Get Contract Variations

-   **GET** `/Api/{project}/ContractVariation/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[ContractVariationDto]

#### Get Contract Variation by ID

-   **GET** `/Api/{project}/ContractVariation/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Variation ID
    -   `project` (string, required): Project identifier
-   **Response:** ContractVariationDto object

#### Get Contract Variations by IDs

-   **GET** `/Api/{project}/ContractVariation/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of variation IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of ContractVariationDto objects

#### Create Contract Variation

-   **POST** `/Api/{project}/ContractVariation/Create`
-   **Parameters:**
    -   `model` (ContractVariationDto, required): Variation data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Update Contract Variation

-   **PUT** `/Api/{project}/ContractVariation/Update`
-   **Parameters:**
    -   `model` (ContractVariationDto, required): Updated variation data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Contract Variation

-   **DELETE** `/Api/{project}/ContractVariation/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Variation ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 13. Control Sheet APIs

#### Get Control Sheets

-   **GET** `/Api/{project}/ControlSheet/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired sheets
    -   `onlyReportable` (boolean, optional): Only reportable sheets
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[ControlSheetDto]

#### Get Salary Control Sheet

-   **GET** `/Api/{project}/ControlSheet/GetSalary`
-   **Parameters:**
    -   `controlSheetId` (int32, required): Control sheet ID
    -   `includeRetired` (boolean, optional): Include retired items
    -   `project` (string, required): Project identifier
-   **Response:** SalaryControlSheetDto object

#### Get Wage Control Sheet

-   **GET** `/Api/{project}/ControlSheet/GetWage`
-   **Parameters:**
    -   `controlSheetId` (int32, required): Control sheet ID
    -   `includeRetired` (boolean, optional): Include retired items
    -   `project` (string, required): Project identifier
-   **Response:** WageControlSheetDto object

#### Get Delay Control Sheet

-   **GET** `/Api/{project}/ControlSheet/GetDelay`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** DelayControlSheetDto object

#### Get Control Sheet Snapshots

-   **GET** `/Api/{project}/ControlSheet/GetSnapshots`
-   **Parameters:**
    -   `timestamp` (int64, required): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** Array of ControlSheetSnapshotDto objects

#### Get Profit Plan

-   **GET** `/Api/{project}/ControlSheet/GetProfitPlan`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** ProfitPlanDto object

#### Get Cash Flow

-   **GET** `/Api/{project}/ControlSheet/GetCashFlow`
-   **Parameters:**
    -   `controlSheetId` (int32, required): Control sheet ID
    -   `project` (string, required): Project identifier
-   **Response:** CashFlowControlSheetDto object

### 14. Cost Code APIs

#### Get Cost Codes

-   **GET** `/Api/{project}/CostCode/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired codes
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[CaCostCodeDto]

#### Get Cost Codes by Document Setting ID

-   **GET** `/Api/{project}/CostCode/GetByDocSettingId`
-   **Parameters:**
    -   `docSettingId` (int32, required): Document setting ID
    -   `includeRetired` (boolean, optional): Include retired codes
    -   `project` (string, required): Project identifier
-   **Response:** Array of CaCostCodeDto objects

#### Create Cost Code

-   **POST** `/Api/{project}/CostCode/Create`
-   **Parameters:**
    -   `model` (CaCostCodeDto, required): Cost code data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Update Cost Code

-   **PUT** `/Api/{project}/CostCode/Update`
-   **Parameters:**
    -   `model` (CaCostCodeDto, required): Updated cost code data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Upsert Cost Code

-   **PUT** `/Api/{project}/CostCode/Upsert`
-   **Parameters:**
    -   `model` (CaCostCodeDto, required): Cost code data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 15. Design Review Issue APIs

#### Get Design Review Issues

-   **GET** `/Api/{project}/DesignReviewIssue/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[DesignReviewIssueDto]

#### Get Design Review Issue by ID

-   **GET** `/Api/{project}/DesignReviewIssue/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Issue ID
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeComments` (boolean, optional): Include comments
    -   `project` (string, required): Project identifier
-   **Response:** DesignReviewIssueDto object

#### Get Design Review Issues by IDs

-   **GET** `/Api/{project}/DesignReviewIssue/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of issue IDs
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeComments` (boolean, optional): Include comments
    -   `project` (string, required): Project identifier
-   **Response:** Array of DesignReviewIssueDto objects

### 16. Document Setting APIs

#### Get Document Settings

-   **GET** `/Api/{project}/DocSetting/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeStatuses` (boolean, optional): Include statuses
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `includeStatusCategories` (boolean, optional): Include status categories
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[DocumentSettingDto]

#### Get Document Settings by IDs

-   **GET** `/Api/{project}/DocSetting/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of document setting IDs
    -   `includeStatuses` (boolean, optional): Include statuses
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `includeStatusCategories` (boolean, optional): Include status categories
    -   `project` (string, required): Project identifier
-   **Response:** Array of DocumentSettingDto objects

#### Get Document Settings by Codes

-   **GET** `/Api/{project}/DocSetting/GetByCodes`
-   **Parameters:**
    -   `codes` (array[string], required): Array of document setting codes
    -   `includeRetired` (boolean, optional): Include retired settings
    -   `includeStatuses` (boolean, optional): Include statuses
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `includeStatusCategories` (boolean, optional): Include status categories
    -   `project` (string, required): Project identifier
-   **Response:** Array of DocumentSettingDto objects

#### Get Document Settings by Type Code

-   **GET** `/Api/{project}/DocSetting/GetByTypeCode`
-   **Parameters:**
    -   `typeCode` (string, required): Type code
    -   `onlyCreatable` (boolean, optional): Only creatable settings
    -   `includeStatuses` (boolean, optional): Include statuses
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `includeStatusCategories` (boolean, optional): Include status categories
    -   `project` (string, required): Project identifier
-   **Response:** Array of DocumentSettingDto objects

#### Get Document Setting Options

-   **GET** `/Api/{project}/DocSetting/GetOptions`
-   **Parameters:**
    -   `docSettingId` (int32, optional): Document setting ID
    -   `docSettingCode` (string, optional): Document setting code
    -   `userFieldId` (int32, optional): User field ID
    -   `userFieldCode` (string, optional): User field code
    -   `project` (string, required): Project identifier
-   **Response:** Array of UserfieldOptionDto objects

#### Add Document Setting Options

-   **POST** `/Api/{project}/DocSetting/AddOptions`
-   **Parameters:**
    -   `options` (array[UserfieldOptionDto], required): Options to add
    -   `docSettingId` (int32, optional): Document setting ID
    -   `docSettingCode` (string, optional): Document setting code
    -   `userFieldId` (int32, optional): User field ID
    -   `userFieldCode` (string, optional): User field code
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Remove Document Setting Options

-   **DELETE** `/Api/{project}/DocSetting/RemoveOptions`
-   **Parameters:**
    -   `options` (array[UserfieldOptionDto], required): Options to remove
    -   `docSettingId` (int32, optional): Document setting ID
    -   `docSettingCode` (string, optional): Document setting code
    -   `userFieldId` (int32, optional): User field ID
    -   `userFieldCode` (string, optional): User field code
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 17. Document APIs

#### Get Documents

-   **GET** `/Api/{project}/Document/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[DocumentDto]

#### Get Documents by Document Code

-   **GET** `/Api/{project}/Document/GetByDocCode`
-   **Parameters:**
    -   `code` (string, required): Document code
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[DocumentDto]

#### Get Document as PDF

-   **GET** `/Api/{project}/Document/GetDocumentAsPdf/{id}`
-   **Parameters:**
    -   `id` (int64, required): Document ID
    -   `chunkId` (int32, optional): Chunk ID for chunked downloads
    -   `relativeLinks` (boolean, optional): Use relative links
    -   `showHistory` (boolean, optional): Show document history
    -   `project` (string, required): Project identifier
-   **Response:** FileChunkDto object

#### Get Document as PDF File

-   **GET** `/Api/{project}/Document/GetDocumentAsPdfFile/{id}`
-   **Parameters:**
    -   `id` (int64, required): Document ID
    -   `relativeLinks` (boolean, optional): Use relative links
    -   `showHistory` (boolean, optional): Show document history
    -   `project` (string, required): Project identifier
-   **Response:** PDF file as byte stream

#### Get Document by ID

-   **GET** `/Api/{project}/Document/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Document ID
    -   `includeComments` (boolean, optional): Include comments
    -   `project` (string, required): Project identifier
-   **Response:** DocumentDto object

#### Get Document by Reference

-   **GET** `/Api/{project}/Document/GetByReference`
-   **Parameters:**
    -   `reference` (string, required): Document reference
    -   `includeComments` (boolean, optional): Include comments
    -   `project` (string, required): Project identifier
-   **Response:** DocumentDto object

#### Get Documents by IDs

-   **GET** `/Api/{project}/Document/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of document IDs
    -   `includeComments` (boolean, optional): Include comments
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `project` (string, required): Project identifier
-   **Response:** Array of DocumentDto objects

#### Search Documents

-   **POST** `/Api/{project}/Document/Search`
-   **Parameters:**
    -   `filter` (Filter, required): Search filter criteria
    -   `project` (string, required): Project identifier
-   **Response:** Array of document IDs (int64[])

#### Create Document

-   **POST** `/Api/{project}/Document/Create`
-   **Parameters:**
    -   `model` (DocumentDto, required): Document data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Split Document

-   **POST** `/Api/{project}/Document/Split`
-   **Parameters:**
    -   `model` (DocumentDto, required): New document data
    -   `splitFromDocumentId` (int64, required): Source document ID
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Update Document

-   **PUT** `/Api/{project}/Document/Update`
-   **Parameters:**
    -   `model` (DocumentDto, required): Updated document data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Import Comment

-   **POST** `/Api/{project}/Document/ImportComment`
-   **Parameters:**
    -   `model` (CommentDto, required): Comment data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Withdraw Document

-   **DELETE** `/Api/{project}/Document/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Document ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 18. External User APIs

#### Get External Users

-   **GET** `/Api/{project}/ExternalUser/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[UserDto]

#### Get External User by ID

-   **GET** `/Api/{project}/ExternalUser/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): User ID
    -   `project` (string, required): Project identifier
-   **Response:** UserDto object

#### Get External Users by IDs

-   **GET** `/Api/{project}/ExternalUser/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of user IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of UserDto objects

### 19. Folder APIs

#### Get Folders

-   **GET** `/Api/{project}/Folder/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[FolderDto]

#### Get Publication Folders

-   **GET** `/Api/{project}/Folder/GetPublication`
-   **Parameters:**
    -   `folderId` (int32, optional): Parent folder ID
    -   `includeSubFolders` (boolean, optional): Include subfolders
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[FolderDto]

### 20. Global Company APIs

#### Get Global Companies

-   **GET** `/Api/GlobalCompany/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
-   **Response:** PageResult[GlobalCompanyDto]

#### Search Global Companies

-   **POST** `/Api/GlobalCompany/Search`
-   **Parameters:**
    -   `companyName` (string, optional): Company name
    -   `businessNo` (string, optional): Business number
    -   `maxResults` (int32, optional): Maximum results
-   **Response:** Array of GlobalCompanyDto objects

#### Get Global Company by ID

-   **GET** `/Api/GlobalCompany/GetById`
-   **Parameters:**
    -   `id` (int32, required): Company ID
-   **Response:** GlobalCompanyDto object

#### Get Global Companies by IDs

-   **GET** `/Api/GlobalCompany/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of company IDs
-   **Response:** Array of GlobalCompanyDto objects

#### Update Global Company

-   **PUT** `/Api/GlobalCompany/Update`
-   **Parameters:**
    -   `model` (GlobalCompanyDto, required): Updated company data
    -   `allProjects` (boolean, optional): Update across all projects
-   **Response:** Result object

### 21. Login APIs

#### Get Login URL

-   **GET** `/Api/Login/GetUrl`
-   **Response:** Login URL string

#### Login by User Token

-   **POST** `/Api/Login/ByUserToken`
-   **Response:** LoginResult object

### 22. Payment Certificate APIs

#### Get Payment Certificates

-   **GET** `/Api/{project}/PaymentCertificate/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[PaymentCertificateDto]

#### Get Payment Certificate by ID

-   **GET** `/Api/{project}/PaymentCertificate/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Certificate ID
    -   `project` (string, required): Project identifier
-   **Response:** PaymentCertificateDto object

#### Get Payment Certificates by IDs

-   **GET** `/Api/{project}/PaymentCertificate/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of certificate IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of PaymentCertificateDto objects

#### Create Payment Certificate

-   **POST** `/Api/{project}/PaymentCertificate/Create`
-   **Parameters:**
    -   `model` (PaymentCertificateDto, required): Certificate data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

### 23. Project APIs

#### Get Projects

-   **GET** `/Api/Project/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
-   **Response:** PageResult[ProjectDto]

#### Get Project by ID

-   **GET** `/Api/Project/GetById`
-   **Parameters:**
    -   `id` (int32, required): Project ID
-   **Response:** ProjectDto object

#### Get Project by Name

-   **GET** `/Api/Project/GetByName`
-   **Parameters:**
    -   `name` (string, required): Project name
-   **Response:** ProjectDto object

#### Get Project Templates

-   **GET** `/Api/Project/GetTemplates`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
-   **Response:** PageResult[ProjectDto]

#### Create Project

-   **POST** `/Api/Project/Create`
-   **Parameters:**
    -   `model` (ProjectDto, required): Project data
-   **Response:** Result object

#### Update Project

-   **PUT** `/Api/Project/Update`
-   **Parameters:**
    -   `model` (ProjectDto, required): Updated project data
-   **Response:** Result object

#### Close Project

-   **DELETE** `/Api/Project/Close`
-   **Parameters:**
    -   `id` (int32, required): Project ID
-   **Response:** Boolean success indicator

### 24. Register Document APIs

#### Get Register Document by ID

-   **GET** `/Api/{project}/RegisterDoc/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Document ID
    -   `includeRevisions` (boolean, optional): Include revisions
    -   `includeLatestRevision` (boolean, optional): Include latest revision
    -   `includeRetired` (boolean, optional): Include retired documents
    -   `includeRetiredRevisions` (boolean, optional): Include retired revisions
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `project` (string, required): Project identifier
-   **Response:** RegisterDocDto object

#### Get Register Document by Name

-   **GET** `/Api/{project}/RegisterDoc/GetByName`
-   **Parameters:**
    -   `name` (string, required): Document name
    -   `fileFormat` (string, optional): File format filter
    -   `includeRevisions` (boolean, optional): Include revisions
    -   `includeLatestRevision` (boolean, optional): Include latest revision
    -   `includeRetired` (boolean, optional): Include retired documents
    -   `includeRetiredRevisions` (boolean, optional): Include retired revisions
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `project` (string, required): Project identifier
-   **Response:** RegisterDocDto object

#### Get Register Documents by Name Pattern

-   **GET** `/Api/{project}/RegisterDoc/GetByNamePattern`
-   **Parameters:**
    -   `searchString` (string, required): Search pattern
    -   `includeRevisions` (boolean, optional): Include revisions
    -   `includeLatestRevision` (boolean, optional): Include latest revision
    -   `includeRetired` (boolean, optional): Include retired documents
    -   `includeRetiredRevisions` (boolean, optional): Include retired revisions
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `project` (string, required): Project identifier
-   **Response:** Array of RegisterDocDto objects

#### Get Register Documents by IDs

-   **GET** `/Api/{project}/RegisterDoc/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of document IDs
    -   `includeRevisions` (boolean, optional): Include revisions
    -   `includeLatestRevision` (boolean, optional): Include latest revision
    -   `includeRetired` (boolean, optional): Include retired documents
    -   `includeRetiredRevisions` (boolean, optional): Include retired revisions
    -   `includeUserFields` (boolean, optional): Include user fields
    -   `project` (string, required): Project identifier
-   **Response:** Array of RegisterDocDto objects

#### Move Register Documents

-   **PUT** `/Api/{project}/RegisterDoc/Move`
-   **Parameters:**
    -   `ids` (array[int64], required): Document IDs to move
    -   `folderId` (int32, required): Target folder ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Retire Register Documents

-   **DELETE** `/Api/{project}/RegisterDoc/Retire`
-   **Parameters:**
    -   `ids` (array[int64], required): Document IDs to retire
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Restore Register Documents

-   **PATCH** `/Api/{project}/RegisterDoc/Restore`
-   **Parameters:**
    -   `ids` (array[int64], required): Document IDs to restore
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 25. Report APIs

#### Create Excel Report

-   **POST** `/Api/{project}/Report/CreateExcel`
-   **Parameters:**
    -   `excelData` (ExcelDataDto, required): Excel data structure
    -   `project` (string, required): Project identifier
-   **Response:** Excel file as byte stream

#### Process Excel File

-   **POST** `/Api/{project}/Report/ProcessExcel`
-   **Parameters:**
    -   `file` (file, required): Excel file to process (multipart/form-data)
    -   `project` (string, required): Project identifier
-   **Response:** ExcelDataDto object

### 26. Revision APIs

#### Get Revision by ID

-   **GET** `/Api/{project}/Revision/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Revision ID
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeRetired` (boolean, optional): Include retired revisions
    -   `project` (string, required): Project identifier
-   **Response:** RevisionDto object

#### Get Revisions by IDs

-   **GET** `/Api/{project}/Revision/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of revision IDs
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeRetired` (boolean, optional): Include retired revisions
    -   `project` (string, required): Project identifier
-   **Response:** Array of RevisionDto objects

#### Get Revisions by Folder ID

-   **GET** `/Api/{project}/Revision/GetByFolderId`
-   **Parameters:**
    -   `folderId` (int32, required): Folder ID
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeRetired` (boolean, optional): Include retired revisions
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[RevisionDto]

#### Get Revisions by Folder IDs

-   **GET** `/Api/{project}/Revision/GetByFolderIds`
-   **Parameters:**
    -   `folderIds` (array[int32], required): Array of folder IDs
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeRetired` (boolean, optional): Include retired revisions
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[RevisionDto]

#### Get Revision Statuses

-   **GET** `/Api/{project}/Revision/GetStatuses`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** Array of ConfigOptionDto objects

#### Get Revision Types

-   **GET** `/Api/{project}/Revision/GetTypes`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** Array of ConfigOptionDto objects

#### Get Revision Disciplines

-   **GET** `/Api/{project}/Revision/GetDisciplines`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** Array of ConfigOptionDto objects

#### Download Revision

-   **GET** `/Api/{project}/Revision/Download/{id}`
-   **Parameters:**
    -   `id` (int32, required): Revision ID
    -   `chunkId` (int32, optional): Chunk ID for chunked downloads
    -   `project` (string, required): Project identifier
-   **Response:** FileChunkDto object

#### Download Revision File

-   **GET** `/Api/{project}/Revision/DownloadFile/{id}`
-   **Parameters:**
    -   `id` (int32, required): Revision ID
    -   `project` (string, required): Project identifier
-   **Response:** File as byte stream

#### Upload Revision

-   **POST** `/Api/{project}/Revision/Upload`
-   **Parameters:**
    -   `folderId` (int32, required): Target folder ID
    -   `fileUpload` (FileChunkDto, required): File data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 27. Saved Search APIs

#### Get Saved Searches

-   **GET** `/Api/{project}/SavedSearch/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[SavedSearchDto]

#### Get Excel Data for Saved Search

-   **GET** `/Api/{project}/SavedSearch/GetExcelData/{id}`
-   **Parameters:**
    -   `id` (int32, required): Saved search ID
    -   `project` (string, required): Project identifier
-   **Response:** ExcelDataDto object

### 28. Security APIs

#### Get Security by ID

-   **GET** `/Api/{project}/Security/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Security ID
    -   `project` (string, required): Project identifier
-   **Response:** SecurityDto object

#### Get Securities by IDs

-   **GET** `/Api/{project}/Security/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of security IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of SecurityDto objects

### 29. Tender Database APIs

#### Get Tender Databases

-   **GET** `/Api/TenderDatabase/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired databases
-   **Response:** PageResult[TenderDatabaseDto]

#### Get Tender Database by ID

-   **GET** `/Api/TenderDatabase/GetById`
-   **Parameters:**
    -   `id` (int32, required): Database ID
    -   `includeRetired` (boolean, optional): Include retired databases
-   **Response:** TenderDatabaseDto object

### 30. Tender Package APIs

#### Get Tender Packages

-   **GET** `/Api/{project}/TenderPackage/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[TenderPackageDto]

#### Get Tender Package by ID

-   **GET** `/Api/{project}/TenderPackage/GetById/{id}`
-   **Parameters:**
    -   `id` (int64, required): Package ID
    -   `project` (string, required): Project identifier
-   **Response:** TenderPackageDto object

#### Get Tender Packages by IDs

-   **GET** `/Api/{project}/TenderPackage/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of package IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of TenderPackageDto objects

#### Create Tender Package

-   **POST** `/Api/{project}/TenderPackage/Create`
-   **Parameters:**
    -   `model` (TenderPackageDto, required): Package data
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Withdraw Tender Package

-   **DELETE** `/Api/{project}/TenderPackage/Withdraw/{id}`
-   **Parameters:**
    -   `id` (int32, required): Package ID
    -   `project` (string, required): Project identifier
-   **Response:** Boolean success indicator

### 31. Transmittal APIs

#### Get Transmittals

-   **GET** `/Api/{project}/Transmittal/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRegisterDoc` (boolean, optional): Include register documents
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[TransmittalDocDto]

#### Get Transmittal by ID

-   **GET** `/Api/{project}/Transmittal/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Transmittal ID
    -   `includeRegisterDoc` (boolean, optional): Include register documents
    -   `project` (string, required): Project identifier
-   **Response:** TransmittalDocDto object

#### Get Transmittals by IDs

-   **GET** `/Api/{project}/Transmittal/GetByIds`
-   **Parameters:**
    -   `ids` (array[int64], required): Array of transmittal IDs
    -   `includeRegisterDoc` (boolean, optional): Include register documents
    -   `project` (string, required): Project identifier
-   **Response:** Array of TransmittalDocDto objects

#### Create Transmittal

-   **POST** `/Api/{project}/Transmittal/Create`
-   **Parameters:**
    -   `model` (TransmittalDocDto, required): Transmittal data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

#### Distribute Transmittal

-   **POST** `/Api/{project}/Transmittal/Distribute`
-   **Parameters:**
    -   `model` (TransmittalDocDto, required): Transmittal data
    -   `sendNotification` (boolean, optional): Send notification
    -   `project` (string, required): Project identifier
-   **Response:** DocumentResult object

### 32. User APIs

#### Get Users

-   **GET** `/Api/{project}/User/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired users
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[UserDto]

#### Get User by ID

-   **GET** `/Api/{project}/User/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): User ID
    -   `project` (string, required): Project identifier
-   **Response:** UserDto object

#### Get User by Code

-   **GET** `/Api/{project}/User/GetByCode`
-   **Parameters:**
    -   `code` (string, required): User code
    -   `project` (string, required): Project identifier
-   **Response:** UserDto object

#### Get Current User

-   **GET** `/Api/{project}/User/GetCurrent`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** UserDto object

#### Get User Groups

-   **GET** `/Api/{project}/User/GetGroups`
-   **Parameters:**
    -   `project` (string, required): Project identifier
-   **Response:** Array of GroupEntityDto objects

#### Create User

-   **POST** `/Api/{project}/User/Create`
-   **Parameters:**
    -   `model` (UserDto, required): User data
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Rename User

-   **PUT** `/Api/{project}/User/Rename/{id}`
-   **Parameters:**
    -   `id` (int32, required): User ID
    -   `newUserCode` (string, required): New user code
    -   `updatePreferCode` (boolean, optional): Update preferred code
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Restore User

-   **PATCH** `/Api/{project}/User/Restore/{id}`
-   **Parameters:**
    -   `id` (int32, required): User ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

#### Retire User

-   **DELETE** `/Api/{project}/User/Retire/{id}`
-   **Parameters:**
    -   `id` (int32, required): User ID
    -   `project` (string, required): Project identifier
-   **Response:** Result object

### 33. Version Set APIs

#### Get Version Sets

-   **GET** `/Api/{project}/VersionSet/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRetired` (boolean, optional): Include retired version sets
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[VersionSetDto]

#### Get Version Set by ID

-   **GET** `/Api/{project}/VersionSet/GetById/{id}`
-   **Parameters:**
    -   `id` (int32, required): Version set ID
    -   `project` (string, required): Project identifier
-   **Response:** VersionSetDto object

#### Get Version Set by Name

-   **GET** `/Api/{project}/VersionSet/GetByName`
-   **Parameters:**
    -   `name` (string, required): Version set name
    -   `project` (string, required): Project identifier
-   **Response:** VersionSetDto object

#### Get Version Sets by IDs

-   **GET** `/Api/{project}/VersionSet/GetByIds`
-   **Parameters:**
    -   `ids` (array[int32], required): Array of version set IDs
    -   `project` (string, required): Project identifier
-   **Response:** Array of VersionSetDto objects

#### Get Version Set Revisions

-   **GET** `/Api/{project}/VersionSet/GetRevisions`
-   **Parameters:**
    -   `versionSetId` (int32, required): Version set ID
    -   `includeRegisterDoc` (boolean, optional): Include register document
    -   `includeRetired` (boolean, optional): Include retired revisions
    -   `project` (string, required): Project identifier
-   **Response:** Array of RevisionDto objects

### 34. Workflow Document APIs

#### Get Workflow Documents

-   **GET** `/Api/{project}/WorkflowDoc/Get`
-   **Parameters:**
    -   `skip` (int32, optional): Number of records to skip
    -   `take` (int32, optional): Number of records to take
    -   `timestamp` (int64, optional): Timestamp filter
    -   `includeRegisterDoc` (boolean, optional): Include register documents
    -   `project` (string, required): Project identifier
-   **Response:** PageResult[WorkflowDocDto]

## Common Data Models

### Result Objects

-   **Result**: Basic operation result with success indicator, messages, and ID
-   **DocumentResult**: Extended result for document operations with reference and link URL
-   **LoginResult**: Login operation result with session key

### Page Results

All paginated responses follow the same structure:

-   `Items`: Array of requested objects
-   `NextPageLink`: URL for next page (if available)
-   `Count`: Total count of items

### Common Document Fields

Most document DTOs share these common fields:

-   `Id`: Unique identifier
-   `DocCode`: Document code
-   `DocTypeCode`: Document type code
-   `Reference`: Document reference
-   `ProjectName`: Project name
-   `StatusName`: Current status name
-   `StatusType`: Status type
-   `Title`: Document title
-   `AuthorCode`: Author user code
-   `AuthorCompanyCode`: Author company code
-   `CreatedDate`: Creation date
-   `IssuedDate`: Issue date
-   `DueDate`: Due date
-   `ClosedDate`: Close date
-   `LastChangedDate`: Last change date
-   `LastModifiedDate`: Last modification date
-   `ActionCodes`: Array of action codes
-   `InfoCodes`: Array of info codes
-   `UserfieldValues`: Array of user field values
-   `Attachments`: Array of attachments
-   `Comments`: Array of comments
-   `Timestamp`: Version timestamp

## Error Handling

The API returns standard HTTP status codes:

-   **200 OK**: Successful request
-   **400 Bad Request**: Invalid request parameters
-   **401 Unauthorized**: Missing or invalid API key
-   **404 Not Found**: Resource not found
-   **500 Internal Server Error**: Server error

## Rate Limiting

Please check with your RIB CX administrator for any rate limiting policies that may apply to your API usage.

## Data Model Definitions

### AnnotationDto

Represents an annotation on a document revision.

-   `Id` (int64): Unique identifier
-   `RevisionId` (int32): Associated revision ID
-   `LayerId` (int64): Layer ID for grouping annotations
-   `LayerName` (string): Layer name
-   `Type` (string): Annotation type (e.g., "Text", "Line", "Rectangle")
-   `Data` (string): Annotation data (JSON format)
-   `CreatedBy` (string): Creator user code
-   `CreatedDate` (datetime): Creation timestamp
-   `ModifiedBy` (string): Last modifier user code
-   `ModifiedDate` (datetime): Last modification timestamp
-   `Color` (string): Annotation color (hex format)
-   `Timestamp` (int64): Version timestamp

### AttachmentDto

Represents a file attachment.

-   `Id` (int32): Unique identifier
-   `DocumentId` (int64): Parent document ID
-   `FileName` (string): Original file name
-   `FileSize` (int64): File size in bytes
-   `FileType` (string): MIME type
-   `UploadedBy` (string): Uploader user code
-   `UploadedDate` (datetime): Upload timestamp
-   `Description` (string): File description
-   `IsRetired` (boolean): Retirement status

### BidderDto

Represents a bidder/tenderer in the system.

-   `Id` (int32): Unique identifier
-   `Code` (string): Bidder code
-   `Name` (string): Bidder name
-   `CompanyId` (int32): Associated company ID
-   `ContactName` (string): Primary contact name
-   `ContactEmail` (string): Contact email
-   `ContactPhone` (string): Contact phone
-   `Status` (string): Bidder status
-   `TenderDatabaseId` (int32): Tender database ID
-   `IsRetired` (boolean): Retirement status
-   `Timestamp` (int64): Version timestamp

### BidderSubmissionDto

Represents a bid submission.

-   `Id` (int64): Unique identifier
-   `BidderId` (int32): Bidder ID
-   `TenderPackageId` (int64): Tender package ID
-   `SubmissionDate` (datetime): Submission date
-   `Amount` (decimal): Bid amount
-   `Currency` (string): Currency code
-   `Status` (string): Submission status
-   `Comments` (string): Submission comments
-   `Attachments` (array[AttachmentDto]): Supporting documents
-   `Timestamp` (int64): Version timestamp

### BudgetDto

Represents a project budget document.

-   Inherits all Common Document Fields
-   `BudgetType` (string): Type of budget
-   `TotalAmount` (decimal): Total budget amount
-   `Currency` (string): Currency code
-   `LineItems` (array[BudgetLineItemDto]): Budget line items
-   `ApprovalStatus` (string): Approval status
-   `ApprovedBy` (string): Approver user code
-   `ApprovedDate` (datetime): Approval date

### BudgetLineItemDto

Represents a budget line item.

-   `Id` (int64): Unique identifier
-   `ItemCode` (string): Line item code
-   `Description` (string): Item description
-   `Quantity` (decimal): Quantity
-   `Unit` (string): Unit of measure
-   `UnitRate` (decimal): Unit rate
-   `Amount` (decimal): Total amount
-   `CostCodeId` (int32): Associated cost code ID
-   `Notes` (string): Additional notes

### BudgetForecastDto

Represents a budget forecast document.

-   Inherits all Common Document Fields
-   `ForecastDate` (datetime): Forecast date
-   `ForecastAmount` (decimal): Forecasted amount
-   `ActualAmount` (decimal): Actual amount to date
-   `VarianceAmount` (decimal): Variance amount
-   `VariancePercentage` (decimal): Variance percentage
-   `ForecastItems` (array[ForecastItemDto]): Forecast line items

### BudgetTransferDto

Represents a budget transfer between items.

-   Inherits all Common Document Fields
-   `FromItemId` (int64): Source line item ID
-   `ToItemId` (int64): Destination line item ID
-   `TransferAmount` (decimal): Transfer amount
-   `Reason` (string): Transfer reason
-   `EffectiveDate` (datetime): Effective date

### BudgetVariationDto

Represents a budget variation document.

-   Inherits all Common Document Fields
-   `VariationType` (string): Type of variation
-   `OriginalAmount` (decimal): Original budget amount
-   `VariationAmount` (decimal): Variation amount
-   `RevisedAmount` (decimal): Revised total amount
-   `Justification` (string): Variation justification
-   `ImpactDescription` (string): Impact description

### ClaimDto

Represents a contractor claim document.

-   Inherits all Common Document Fields
-   `ContractId` (int64): Associated contract ID
-   `ClaimType` (string): Type of claim
-   `ClaimAmount` (decimal): Claim amount
-   `ClaimDate` (datetime): Claim date
-   `DaysExtension` (int32): Days extension requested
-   `ClaimItems` (array[ClaimItemDto]): Claim line items
-   `SupportingDocuments` (array[AttachmentDto]): Supporting documents

### CompanyDto

Represents a company entity.

-   `Id` (int32): Unique identifier
-   `Code` (string): Company code
-   `Name` (string): Company name
-   `BusinessNumber` (string): Business registration number
-   `TradingAs` (string): Trading name
-   `CompanyType` (string): Company type
-   `Roles` (array[string]): Company roles in project
-   `Address` (AddressDto): Company address
-   `ContactDetails` (ContactDto): Primary contact
-   `IsRetired` (boolean): Retirement status
-   `Timestamp` (int64): Version timestamp

### CompanyRoleDto

Represents a company role configuration.

-   `Id` (int32): Unique identifier
-   `Code` (string): Role code
-   `Name` (string): Role name
-   `Description` (string): Role description
-   `Permissions` (array[string]): Associated permissions
-   `IsRetired` (boolean): Retirement status

### ContractDto

Represents a contract document.

-   Inherits all Common Document Fields
-   `ContractorId` (int32): Contractor company ID
-   `ContractType` (string): Type of contract
-   `ContractAmount` (decimal): Contract amount
-   `RetentionPercentage` (decimal): Retention percentage
-   `DefectsLiabilityPeriod` (int32): Defects liability period (days)
-   `CommencementDate` (datetime): Contract start date
-   `CompletionDate` (datetime): Contract end date
-   `ContractItems` (array[ContractItemDto]): Contract line items

### ContractVariationDto

Represents a contract variation document.

-   Inherits all Common Document Fields
-   `ContractId` (int64): Parent contract ID
-   `VariationNumber` (int32): Variation sequence number
-   `VariationType` (string): Type of variation
-   `OriginalAmount` (decimal): Original contract amount
-   `VariationAmount` (decimal): Variation amount
-   `RevisedAmount` (decimal): Revised contract amount
-   `DaysExtension` (int32): Time extension (days)
-   `VariationItems` (array[VariationItemDto]): Variation line items

### ControlSheetDto

Represents a control sheet for project monitoring.

-   `Id` (int32): Unique identifier
-   `Code` (string): Control sheet code
-   `Name` (string): Control sheet name
-   `Type` (string): Control sheet type
-   `ReportingPeriod` (string): Reporting period
-   `IsReportable` (boolean): Reportable flag
-   `IsRetired` (boolean): Retirement status
-   `LastUpdated` (datetime): Last update timestamp
-   `Timestamp` (int64): Version timestamp

### CaCostCodeDto

Represents a cost allocation code.

-   `Id` (int32): Unique identifier
-   `Code` (string): Cost code
-   `Description` (string): Cost code description
-   `Category` (string): Cost category
-   `ParentId` (int32): Parent cost code ID
-   `Level` (int32): Hierarchy level
-   `IsRetired` (boolean): Retirement status
-   `Timestamp` (int64): Version timestamp

### DesignReviewIssueDto

Represents a design review issue.

-   `Id` (int32): Unique identifier
-   `IssueNumber` (string): Issue reference number
-   `Title` (string): Issue title
-   `Description` (string): Issue description
-   `Category` (string): Issue category
-   `Priority` (string): Priority level
-   `Status` (string): Current status
-   `RaisedBy` (string): Raiser user code
-   `RaisedDate` (datetime): Date raised
-   `RegisterDocId` (int32): Associated register document
-   `RevisionId` (int32): Associated revision
-   `Comments` (array[CommentDto]): Issue comments
-   `Attachments` (array[AttachmentDto]): Supporting files

### DocumentSettingDto

Represents document type configuration.

-   `Id` (int32): Unique identifier
-   `Code` (string): Document type code
-   `Name` (string): Document type name
-   `TypeCode` (string): Parent type code
-   `IsCreatable` (boolean): Can create new documents
-   `RequiresApproval` (boolean): Requires approval workflow
-   `Statuses` (array[StatusDto]): Available statuses
-   `UserFields` (array[UserFieldDto]): Custom fields
-   `StatusCategories` (array[StatusCategoryDto]): Status categories
-   `IsRetired` (boolean): Retirement status

### DocumentDto

Base class for all document types.

-   `Id` (int64): Unique identifier
-   `DocCode` (string): Document code
-   `DocTypeCode` (string): Document type code
-   `Reference` (string): Document reference
-   `ProjectName` (string): Project name
-   `StatusName` (string): Current status
-   `StatusType` (string): Status type
-   `Title` (string): Document title
-   `AuthorCode` (string): Author user code
-   `AuthorCompanyCode` (string): Author company code
-   `CreatedDate` (datetime): Creation date
-   `IssuedDate` (datetime): Issue date
-   `DueDate` (datetime): Due date
-   `ClosedDate` (datetime): Close date
-   `LastChangedDate` (datetime): Last change date
-   `LastModifiedDate` (datetime): Last modification date
-   `ActionCodes` (array[string]): Available actions
-   `InfoCodes` (array[string]): Information codes
-   `UserfieldValues` (array[UserfieldValueDto]): Custom field values
-   `Attachments` (array[AttachmentDto]): File attachments
-   `Comments` (array[CommentDto]): Document comments
-   `Timestamp` (int64): Version timestamp

### CommentDto

Represents a document comment.

-   `Id` (int64): Unique identifier
-   `DocumentId` (int64): Parent document ID
-   `CommentText` (string): Comment text
-   `CommentBy` (string): Commenter user code
-   `CommentDate` (datetime): Comment timestamp
-   `IsInternal` (boolean): Internal comment flag
-   `ParentCommentId` (int64): Parent comment for threading

### ExcelDataDto

Represents Excel report data structure.

-   `Sheets` (array[SheetDataDto]): Excel sheets
-   `FileName` (string): Output file name
-   `Template` (string): Template name

### SheetDataDto

Represents Excel sheet data.

-   `SheetName` (string): Sheet name
-   `Headers` (array[string]): Column headers
-   `Rows` (array[array[object]]): Data rows
-   `ColumnWidths` (array[int32]): Column widths
-   `FreezePanes` (boolean): Freeze header row

### FileChunkDto

Represents file data for chunked transfers.

-   `ChunkId` (int32): Chunk identifier
-   `TotalChunks` (int32): Total number of chunks
-   `FileName` (string): File name
-   `FileSize` (int64): Total file size
-   `ChunkData` (string): Base64 encoded chunk data
-   `IsLastChunk` (boolean): Last chunk indicator

### Filter

Represents search filter criteria.

-   `Field` (string): Field name to filter
-   `Operator` (string): Filter operator (eq, ne, gt, lt, contains, etc.)
-   `Value` (object): Filter value
-   `And` (array[Filter]): AND conditions
-   `Or` (array[Filter]): OR conditions

### FolderDto

Represents a document folder.

-   `Id` (int32): Unique identifier
-   `Name` (string): Folder name
-   `Path` (string): Full folder path
-   `ParentId` (int32): Parent folder ID
-   `FolderType` (string): Folder type
-   `IsPublic` (boolean): Public access flag
-   `Permissions` (array[string]): Folder permissions
-   `Timestamp` (int64): Version timestamp

### GlobalCompanyDto

Represents a global company across projects.

-   `Id` (int32): Unique identifier
-   `Name` (string): Company name
-   `BusinessNumber` (string): Business registration
-   `Country` (string): Country code
-   `IsActive` (boolean): Active status
-   `Projects` (array[string]): Associated projects
-   `LastUpdated` (datetime): Last update timestamp

### GroupEntityDto

Represents a user group.

-   `Id` (int32): Unique identifier
-   `Code` (string): Group code
-   `Name` (string): Group name
-   `Description` (string): Group description
-   `Members` (array[string]): Member user codes
-   `Permissions` (array[string]): Group permissions

### LoginResult

Represents login operation result.

-   `Success` (boolean): Success indicator
-   `SessionKey` (string): Session key for API calls
-   `ExpiresAt` (datetime): Session expiration
-   `UserCode` (string): Logged in user code
-   `Projects` (array[string]): Available projects

### NumberInfoDto

Represents budget line item details.

-   `LineItemId` (int64): Line item ID
-   `ItemCode` (string): Item code
-   `Description` (string): Item description
-   `Quantity` (decimal): Quantity
-   `Unit` (string): Unit of measure
-   `Rate` (decimal): Unit rate
-   `Amount` (decimal): Total amount
-   `CostCode` (string): Associated cost code
-   `BudgetId` (int64): Parent budget ID

### PageResult[T]

Generic paginated result container.

-   `Items` (array[T]): Page items
-   `NextPageLink` (string): URL for next page
-   `Count` (int32): Total item count

### PaymentCertificateDto

Represents a payment certificate document.

-   Inherits all Common Document Fields
-   `ContractId` (int64): Associated contract ID
-   `CertificateNumber` (int32): Certificate sequence number
-   `PeriodFrom` (datetime): Period start date
-   `PeriodTo` (datetime): Period end date
-   `WorkCompleted` (decimal): Value of work completed
-   `MaterialsOnSite` (decimal): Materials on site value
-   `TotalClaimed` (decimal): Total amount claimed
-   `PreviousCertified` (decimal): Previously certified amount
-   `CurrentClaim` (decimal): Current claim amount
-   `Retention` (decimal): Retention amount
-   `NetPayment` (decimal): Net payment due

### ProjectDto

Represents a project.

-   `Id` (int32): Unique identifier
-   `Name` (string): Project name
-   `Code` (string): Project code
-   `Description` (string): Project description
-   `Status` (string): Project status
-   `StartDate` (datetime): Project start date
-   `EndDate` (datetime): Project end date
-   `ProjectValue` (decimal): Total project value
-   `Currency` (string): Project currency
-   `IsTemplate` (boolean): Template project flag
-   `CreatedDate` (datetime): Creation date
-   `Settings` (ProjectSettingsDto): Project settings

### RegisterDocDto

Represents a document in the register.

-   `Id` (int32): Unique identifier
-   `Name` (string): Document name
-   `Title` (string): Document title
-   `FileFormat` (string): File format/extension
-   `FolderId` (int32): Parent folder ID
-   `Discipline` (string): Document discipline
-   `DocumentType` (string): Document type
-   `IsRetired` (boolean): Retirement status
-   `Revisions` (array[RevisionDto]): Document revisions
-   `LatestRevision` (RevisionDto): Latest revision
-   `UserFields` (array[UserfieldValueDto]): Custom fields
-   `Timestamp` (int64): Version timestamp

### Result

Basic operation result.

-   `Success` (boolean): Success indicator
-   `Messages` (array[string]): Result messages
-   `Id` (int64): Created/updated entity ID

### DocumentResult

Extended result for document operations.

-   Inherits all Result fields
-   `Reference` (string): Document reference
-   `LinkUrl` (string): Document URL

### RevisionDto

Represents a document revision.

-   `Id` (int32): Unique identifier
-   `RegisterDocId` (int32): Parent document ID
-   `RevisionCode` (string): Revision code
-   `Status` (string): Revision status
-   `Type` (string): Revision type
-   `Description` (string): Revision description
-   `FileSize` (int64): File size in bytes
-   `UploadedBy` (string): Uploader user code
-   `UploadedDate` (datetime): Upload date
-   `IssuedDate` (datetime): Issue date
-   `IsRetired` (boolean): Retirement status
-   `RegisterDoc` (RegisterDocDto): Parent document
-   `Annotations` (array[AnnotationDto]): Revision annotations

### SavedSearchDto

Represents a saved search configuration.

-   `Id` (int32): Unique identifier
-   `Name` (string): Search name
-   `Description` (string): Search description
-   `SearchType` (string): Type of search
-   `Filter` (Filter): Search filter criteria
-   `Columns` (array[string]): Display columns
-   `SortBy` (string): Sort field
-   `SortOrder` (string): Sort order (asc/desc)
-   `IsPublic` (boolean): Public search flag
-   `CreatedBy` (string): Creator user code
-   `CreatedDate` (datetime): Creation date

### SecurityDto

Represents security/permission configuration.

-   `Id` (int32): Unique identifier
-   `EntityType` (string): Entity type (User, Group, Company)
-   `EntityId` (int32): Entity ID
-   `Permissions` (array[string]): Granted permissions
-   `DeniedPermissions` (array[string]): Explicitly denied permissions
-   `EffectiveFrom` (datetime): Effective start date
-   `EffectiveTo` (datetime): Effective end date

### StatusDto

Represents a document status configuration.

-   `Id` (int32): Unique identifier
-   `Code` (string): Status code
-   `Name` (string): Status name
-   `Category` (string): Status category
-   `IsDefault` (boolean): Default status flag
-   `AllowedTransitions` (array[string]): Allowed next statuses
-   `RequiresComment` (boolean): Requires comment on transition

### TenderDatabaseDto

Represents a tender/bidder database.

-   `Id` (int32): Unique identifier
-   `Name` (string): Database name
-   `Description` (string): Database description
-   `IsGlobal` (boolean): Global database flag
-   `ProjectIds` (array[int32]): Associated projects
-   `IsRetired` (boolean): Retirement status
-   `Timestamp` (int64): Version timestamp

### TenderPackageDto

Represents a tender package document.

-   Inherits all Common Document Fields
-   `PackageCode` (string): Package code
-   `PackageType` (string): Package type
-   `EstimatedValue` (decimal): Estimated value
-   `TenderCloseDate` (datetime): Tender closing date
-   `EvaluationDate` (datetime): Evaluation date
-   `AwardDate` (datetime): Award date
-   `Bidders` (array[BidderDto]): Invited bidders
-   `Submissions` (array[BidderSubmissionDto]): Received submissions

### TransmittalDocDto

Represents a transmittal document.

-   Inherits all Common Document Fields
-   `TransmittalNumber` (string): Transmittal number
-   `RecipientCompanyCode` (string): Recipient company
-   `RecipientUserCode` (string): Recipient user
-   `TransmittalDate` (datetime): Transmittal date
-   `Purpose` (string): Transmittal purpose
-   `RegisterDocs` (array[RegisterDocDto]): Transmitted documents
-   `RevisionIds` (array[int32]): Transmitted revision IDs
-   `ResponseRequired` (boolean): Response required flag
-   `ResponseDueDate` (datetime): Response due date

### UserDto

Represents a system user.

-   `Id` (int32): Unique identifier
-   `Code` (string): User code
-   `Name` (string): Full name
-   `Email` (string): Email address
-   `CompanyCode` (string): Company code
-   `UserType` (string): User type (Internal/External)
-   `Groups` (array[string]): Group memberships
-   `IsActive` (boolean): Active status
-   `IsRetired` (boolean): Retirement status
-   `LastLogin` (datetime): Last login timestamp
-   `Timestamp` (int64): Version timestamp

### UserfieldOptionDto

Represents a custom field option.

-   `Id` (int32): Unique identifier
-   `Value` (string): Option value
-   `DisplayText` (string): Display text
-   `SortOrder` (int32): Sort order
-   `IsDefault` (boolean): Default option flag
-   `IsRetired` (boolean): Retirement status

### UserfieldValueDto

Represents a custom field value.

-   `FieldId` (int32): Field ID
-   `FieldCode` (string): Field code
-   `FieldName` (string): Field name
-   `FieldType` (string): Field type (Text, Number, Date, List)
-   `Value` (object): Field value
-   `DisplayValue` (string): Formatted display value

### VersionSetDto

Represents a version set for document control.

-   `Id` (int32): Unique identifier
-   `Name` (string): Version set name
-   `Description` (string): Version set description
-   `CreatedBy` (string): Creator user code
-   `CreatedDate` (datetime): Creation date
-   `IsLocked` (boolean): Locked status
-   `IsRetired` (boolean): Retirement status
-   `RevisionCount` (int32): Number of revisions
-   `Timestamp` (int64): Version timestamp

### WorkflowDocDto

Represents a workflow document.

-   Inherits all Common Document Fields
-   `WorkflowType` (string): Workflow type
-   `CurrentStep` (string): Current workflow step
-   `CurrentAssignee` (string): Current assignee
-   `WorkflowStatus` (string): Workflow status
-   `Steps` (array[WorkflowStepDto]): Workflow steps
-   `History` (array[WorkflowHistoryDto]): Workflow history

### WorkflowStepDto

Represents a workflow step.

-   `StepNumber` (int32): Step sequence number
-   `StepName` (string): Step name
-   `AssigneeCode` (string): Assignee user code
-   `Action` (string): Required action
-   `Status` (string): Step status
-   `CompletedDate` (datetime): Completion date
-   `Comments` (string): Step comments
-   `DueDate` (datetime): Step due date

### AddressDto

Represents a physical address.

-   `AddressLine1` (string): Address line 1
-   `AddressLine2` (string): Address line 2
-   `City` (string): City
-   `State` (string): State/Province
-   `PostalCode` (string): Postal/Zip code
-   `Country` (string): Country code

### ContactDto

Represents contact information.

-   `ContactName` (string): Contact person name
-   `ContactTitle` (string): Contact title/position
-   `ContactEmail` (string): Email address
-   `ContactPhone` (string): Phone number
-   `ContactMobile` (string): Mobile number
-   `ContactFax` (string): Fax number

## Support

For API support and additional documentation, please contact your RIB CX administrator or
