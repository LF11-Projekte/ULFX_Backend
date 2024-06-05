/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** Comment */
export interface Comment {
  /** Content */
  content: string;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** Me */
export interface Me {
  /** Displayname */
  displayname?: string | null;
  /** Description */
  description?: string | null;
}

/** Post */
export interface Post {
  /** Thumbnail */
  thumbnail: string;
  /** Teaser */
  teaser: string;
  /** Title */
  title: string;
  /** Content */
  content: string;
}

/** PutPost */
export interface PutPost {
  /** Thumbnail */
  thumbnail?: string | null;
  /** Teaser */
  teaser?: string | null;
  /** Title */
  title?: string | null;
  /** Content */
  content?: string | null;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title FastAPI
 * @version 0.1.0
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  /**
   * No description
   *
   * @name RootGet
   * @summary Root
   * @request GET:/
   */
  rootGet = (params: RequestParams = {}) =>
    this.request<any, any>({
      path: `/`,
      method: "GET",
      format: "json",
      ...params,
    });

  auth = {
    /**
     * No description
     *
     * @tags auth
     * @name GetAuthLoginAuthLoginGet
     * @summary Get Auth Login
     * @request GET:/auth/login
     */
    getAuthLoginAuthLoginGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/auth/login`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags auth
     * @name GetAuthLoginAuthLogoutGet
     * @summary Get Auth Login
     * @request GET:/auth/logout
     */
    getAuthLoginAuthLogoutGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/auth/logout`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags auth
     * @name GetAuthTokenAuthTokenGet
     * @summary Get Auth Token
     * @request GET:/auth/token
     */
    getAuthTokenAuthTokenGet: (
      query?: {
        /**
         * Token
         * @default ""
         */
        token?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/auth/token`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),
  };
  user = {
    /**
     * No description
     *
     * @tags user
     * @name GetUserUserMeGet
     * @summary Get User
     * @request GET:/user/me
     */
    getUserUserMeGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/user/me`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags user
     * @name GetUserUserMePut
     * @summary Get User
     * @request PUT:/user/me/
     */
    getUserUserMePut: (data: Me, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/user/me/`,
        method: "PUT",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags user
     * @name GetUserByIdUserByIdIdGet
     * @summary Get User By Id
     * @request GET:/user/byId/:id
     */
    getUserByIdUserByIdIdGet: (
      id: string,
      query: {
        /** User Id */
        user_id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/user/byId/${id}`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),
  };
  post = {
    /**
     * No description
     *
     * @tags post
     * @name GetNewestPostPostPost
     * @summary Get Newest Post
     * @request POST:/post/
     */
    getNewestPostPostPost: (data: Post, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/post/`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags post
     * @name GetNewestPostPostIdPut
     * @summary Get Newest Post
     * @request PUT:/post/:id
     */
    getNewestPostPostIdPut: (
      id: string,
      query: {
        /** Post Id */
        post_id: number;
      },
      data: PutPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/post/${id}`,
        method: "PUT",
        query: query,
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags post
     * @name GetNewestPostPostNewestGet
     * @summary Get Newest Post
     * @request GET:/post/newest
     */
    getNewestPostPostNewestGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/post/newest`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags post
     * @name GetPostByIdPostByIdIdGet
     * @summary Get Post By Id
     * @request GET:/post/byId/:id
     */
    getPostByIdPostByIdIdGet: (
      id: string,
      query: {
        /** Post Id */
        post_id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/post/byId/${id}`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags post
     * @name GetPostOfFollowedPostFollowedGet
     * @summary Get Post Of Followed
     * @request GET:/post/followed
     */
    getPostOfFollowedPostFollowedGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/post/followed`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
  follower = {
    /**
     * No description
     *
     * @tags follower
     * @name GetFollowersOfUserFollowerOfUserIdGet
     * @summary Get Followers Of User
     * @request GET:/follower/ofUser/:id
     */
    getFollowersOfUserFollowerOfUserIdGet: (
      id: string,
      query: {
        /** User Id */
        user_id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/follower/ofUser/${id}`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags follower
     * @name GetFollowersOfUserFollowerFollowIdPost
     * @summary Get Followers Of User
     * @request POST:/follower/follow/:id
     */
    getFollowersOfUserFollowerFollowIdPost: (
      id: string,
      query: {
        /** Follow Id */
        follow_id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/follower/follow/${id}`,
        method: "POST",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags follower
     * @name GetFollowersOfUserFollowerUnfollowIdPost
     * @summary Get Followers Of User
     * @request POST:/follower/unfollow/:id
     */
    getFollowersOfUserFollowerUnfollowIdPost: (
      id: string,
      query: {
        /** Follow Id */
        follow_id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/follower/unfollow/${id}`,
        method: "POST",
        query: query,
        format: "json",
        ...params,
      }),
  };
  search = {
    /**
     * No description
     *
     * @tags search
     * @name GetSearchSearchGet
     * @summary Get Search
     * @request GET:/search/
     */
    getSearchSearchGet: (
      query?: {
        /** Aduser */
        aduser?: string;
        /** Title */
        title?: string;
        /** Teaser */
        teaser?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/search/`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),
  };
  comment = {
    /**
     * No description
     *
     * @tags comments
     * @name GetCommentsOfPostCommentOfPostIdGet
     * @summary Get Comments Of Post
     * @request GET:/comment/ofPost/:id
     */
    getCommentsOfPostCommentOfPostIdGet: (
      id: string,
      query: {
        /** Post Id */
        post_id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/comment/ofPost/${id}`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags comments
     * @name CommentPostCommentPostIdPost
     * @summary Comment Post
     * @request POST:/comment/post/:id
     */
    commentPostCommentPostIdPost: (
      id: string,
      query: {
        /** Post Id */
        post_id: number;
      },
      data: Comment,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/comment/post/${id}`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags comments
     * @name CommentPostCommentCommentIdPost
     * @summary Comment Post
     * @request POST:/comment/comment/:id
     */
    commentPostCommentCommentIdPost: (
      id: string,
      query: {
        /** Comment Id */
        comment_id: number;
      },
      data: Comment,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/comment/comment/${id}`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags comments
     * @name CommentPostCommentIdPut
     * @summary Comment Post
     * @request PUT:/comment/:id
     */
    commentPostCommentIdPut: (
      id: string,
      query: {
        /** Comment Id */
        comment_id: number;
      },
      data: Comment,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/comment/${id}`,
        method: "PUT",
        query: query,
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
}
