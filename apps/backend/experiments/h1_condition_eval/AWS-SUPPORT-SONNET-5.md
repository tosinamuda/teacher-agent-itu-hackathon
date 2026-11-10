# AWS Support / Sales case — Claude Sonnet 5 refused despite all control-plane checks green

**Account ID:** 083804847775
**Region:** us-east-1
**Model:** `anthropic.claude-sonnet-5`
**Related quota case:** 178721691000814
**Date:** 2026-08-20

## Summary

`anthropic.claude-sonnet-5` returns `AccessDeniedException` — *"not available for this
account … contact AWS Sales"* — on both the `bedrock-runtime` and `bedrock-mantle`
endpoints, while `GetFoundationModelAvailability` reports every field as available and a
foundation model agreement has been created successfully.

Other Anthropic models on the same account, same region, same credentials and same code
path work correctly, so this is not an IAM, region, endpoint or client problem.

## What GetFoundationModelAvailability returns

```
$ aws bedrock get-foundation-model-availability \
    --region us-east-1 --model-id anthropic.claude-sonnet-5
{
    "modelId": "anthropic.claude-sonnet-5",
    "agreementAvailability": { "status": "AVAILABLE" },
    "authorizationStatus": "AUTHORIZED",
    "entitlementAvailability": "AVAILABLE",
    "regionAvailability": "AVAILABLE"
}
```

All four checks pass. Invocation still fails.

## The errors

**bedrock-runtime, via the global inference profile:**

```
$ aws bedrock-runtime converse --model-id global.anthropic.claude-sonnet-5 \
    --messages '[{"role":"user","content":[{"text":"say OK"}]}]'

An error occurred (AccessDeniedException) when calling the Converse operation:
anthropic.claude-sonnet-5 is not available for this account. You can explore other
available models on Amazon Bedrock. For additional access options, contact AWS Sales
at https://aws.amazon.com/contact-us/sales-support/
```

Identical for `us.anthropic.claude-sonnet-5` and for the bare model id.

**bedrock-mantle, Anthropic-compatible endpoint:**

```
POST https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages
{"model":"anthropic.claude-sonnet-5", ...}

{"type":"error",
 "request_id":"req_ziydujkgmfwnizo3232cygvjx4iy2kwshal4rrfvq3ryitmomeja",
 "error":{"type":"permission_error",
          "message":"anthropic.claude-sonnet-5 is not available for this account. ..."}}
```

Also seen: `req_nma34a5b6kjtslkefheavne4z35xeyqsmp4zlpywbiirft2655ia`.

The AWS console playground (Bedrock → Playground → Claude Sonnet 5) shows the same
`AccessDeniedException`, so it reproduces outside our code entirely.

## What was already tried

1. **Foundation model agreement — created, made no difference.**
   `agreementAvailability` moved `NOT_AVAILABLE` → `PENDING` → `AVAILABLE`:
   ```
   aws bedrock list-foundation-model-agreement-offers \
       --model-id anthropic.claude-sonnet-5 --offer-type ALL     # offer-2ykemehpsyf7g
   aws bedrock create-foundation-model-agreement \
       --model-id anthropic.claude-sonnet-5 --offer-token <token>
   ```
   Invocation was retried for 10 minutes afterwards (20 attempts). Still refused.

2. **IAM permissions — confirmed sufficient.** The calling principal
   `arn:aws:iam::083804847775:user/BedrockAPIKey-y1lw` holds `AmazonBedrockLimitedAccess`,
   `AmazonBedrockMarketplaceAccess`, and inline grants for
   `bedrock:CreateFoundationModelAgreement`, `bedrock:PutUseCaseForModelAccess`,
   `aws-marketplace:Subscribe`, `aws-marketplace:ViewSubscriptions` and
   `servicequotas:*`. An IAM denial reports *"is not authorized to perform &lt;action&gt;"*;
   these errors do not, and the same principal invokes other Anthropic models
   successfully.

3. **Quota increases — filed and auto-denied in 85 seconds.** All four adjustable Sonnet 5
   quotas were requested at exactly the AWS default value:

   | quota code | quota | applied | requested |
   |---|---|---|---|
   | `L-38EB0A61` | [bedrock-mantle] Input TPM, Claude Sonnet 5 | 0 | 3,000,000 |
   | `L-15830237` | [bedrock-mantle] Output TPM, Claude Sonnet 5 | 0 | 300,000 |
   | `L-DD84E5CA` | Global cross-region inference TPM | 0 | 6,000,000 |
   | `L-D4FBCF4E` | Cross-region inference TPM | 0 | 6,000,000 |

   All four went `PENDING` → `CASE_CLOSED` within 85 seconds with the applied value still
   `0.0`. Case id **178721691000814**.

4. **Anthropic first-time-use form.** The console offers it (Bedrock → Playground →
   Claude Sonnet 5). It was not submitted, because `authorizationStatus` already reports
   `AUTHORIZED` and `create-foundation-model-agreement` succeeded without requesting it.
   The AWS documentation also states the FTU requirement "does not apply to Anthropic
   models accessed through the `bedrock-mantle` endpoint", and mantle refuses the model
   too. **If submitting the form would change anything here, please say so and we will.**

5. **Inference profiles.** `global.` and `us.` profiles both exist and are `ACTIVE` for
   Sonnet 5; both are refused. Not a profile-addressing problem — the same profile form
   works for other models (below).

## The contrast that isolates it

Same account, region, credentials, endpoint and command — only the model id differs:

| inference profile | result |
|---|---|
| `global.anthropic.claude-sonnet-4-6` | **works** |
| `global.anthropic.claude-sonnet-4-5-20250929-v1:0` | **works** |
| `global.anthropic.claude-opus-4-6-v1` | **works** |
| `global.anthropic.claude-opus-4-5-20251101-v1:0` | **works** |
| `global.anthropic.claude-haiku-4-5-20251001-v1:0` | **works** |
| `global.anthropic.claude-sonnet-5` | AccessDenied |
| `global.anthropic.claude-opus-5` | AccessDenied |
| `global.anthropic.claude-opus-4-8` | AccessDenied |
| `global.anthropic.claude-opus-4-7` | AccessDenied |
| `global.anthropic.claude-fable-5` | AccessDenied |

The split falls exactly on model generation, not on anything account-, region- or
permission-shaped. `openai.gpt-5.6-luna` behaves the same way: agreement created and
active, mantle quota at its full 20,000,000, still `AccessDenied`.

## What we are asking

1. Confirm whether an account-level eligibility gate applies to this account for the
   Claude 5 generation (and GPT-5.x), separate from agreement, entitlement and quota.
2. If so, what the criteria are and how to request access.
3. If the Anthropic first-time-use form would resolve it, confirm that and we will submit
   it immediately.

## Use case

Non-commercial MSc dissertation research (University of Lagos). The model is used only as
a blinded rubric judge scoring anonymised, generated revision packs against four fixed
criteria — roughly 150 calls per experimental run, a few hundred thousand tokens in total.
It does not generate student-facing content and is not deployed to end users.

Work continues on Claude Sonnet 4.5 meanwhile; this request is about whether the Claude 5
generation can be made available at all.
